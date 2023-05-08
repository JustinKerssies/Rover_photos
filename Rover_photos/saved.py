"""
    Creates a Saved Button and has all the functions that have to do with the saved images
"""

from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
from _saved_tab import Saved_tab
from image import Photo


class Saved(Button):

    def __init__(self, UI=None, master=None):
        # create a button
        super().__init__(master=master)
        self.master = master
        self.UI = UI
        master.pack_propagate(False)
        master.update()
        self.size = master.winfo_width(), master.winfo_height()
        search_button = Button(master, text='saved', command=self.clicked)
        search_button.pack(expand=True, fill='both')

    def clicked(self):
        tab = Saved_tab(self.master, self.size)
        if not tab.cancel:
            data = tab.data

            empty = True
            for items in data:
                if not data[items] == '':
                    empty = False

            self.UI.var_data.initialize()
            self.search_through_favorites(empty, data)
            self.UI.create_image_data()
        else:
            pass
        try:
            tab.saved_tab.destroy()
        except TclError:
            pass

    def search_through_favorites(self, empty, user_input):
        # If the entire search parameter is empty, simply load the entirety of the 'fav_data.txt'
        if empty:
            self.create_data_from_fav_file()
            # If there were no ID's in 'fav_data.txt', the file is most probably empty, therefore return an error
            if len(self.UI.var_data.id_list) == 0:
                messagebox.showinfo('Error', 'No favorites yet')
                return

        # If there are search parameters, save the inputs into s.favorite_sorting_list as
        # {classification : value, .......}
        else:
            for item in user_input:
                self.UI.var_data.favorite_sorting_list[item] = user_input[item]
            # Initiate the search for specific photos
            self.create_data_for_specific_fav_photo()
            # If no Photos could be found with the specific parameters, return an error
            if len(self.UI.var_data.id_list) == 0:
                messagebox.showinfo('Error', 'Cannot find specific photo')
                return

    def retrieve_fav_ids(self):
        # Create a list with all the ID's that have been categorized as 'Favorite'
        fav_ids = []

        # Open 'Fav_Data.txt', which is the file that contains all the data for the favorite photos
        with open('fav_data.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                # Create a separation between classification ('ID') with the value ('100023')
                temp_separation = line.split(':', 2)
                # If the classification == 'id', strip the value from any unnecessary symbols
                if 'id' in temp_separation[0]:
                    id_value = temp_separation[1].strip("' \n")
                    # Save the ID value as an integer in the list with all the favorite ID's
                    fav_ids.append(int(id_value))

        # Save the list within "data.py" for easy retrieval
        self.UI.var_data.fav_list = fav_ids

    def create_data_from_fav_file(self):
        # Open Fav_data.txt as readable
        with open('fav_data.txt', 'r') as f:
            # Create lines and a temporary dictionary to save
            lines = f.readlines()
            self.fav_data_sorting(lines)

    def create_data_for_specific_fav_photo(self):
        # Variable which determines whether, once you reach &END_PHOTO, it should save the lines
        remove_variable = True
        # Temporary Library for lines, that get emptied after each &END_PHOTO
        temp_lib = []
        # Library to save any the lines, if any of the search parameters overlap with the line
        saved_photo = []
        print(self.UI.var_data.favorite_sorting_list)
        # Make everything lower_case, to make sure Caps don't cause trouble
        for item in self.UI.var_data.favorite_sorting_list:
            self.UI.var_data.favorite_sorting_list[item] = self.UI.var_data.favorite_sorting_list[item].lower()
        with open('fav_data.txt', 'r') as f:
            # A library that contains either 0 or 1's, based on if both the classification and the value are in the line
            # This is to make sure that you can have multiple search parameters at once, and that it only shows photos
            # that abide by all rules
            okay_lib = []
            lines = f.readlines()
            for line in lines:
                temp_lib.append(line)
                for item in self.UI.var_data.favorite_sorting_list:
                    # Check for every item, whether the classification is in the line
                    if str(item).lower() in line.lower():
                        # Check if the value is also contained within the line
                        if str(self.UI.var_data.favorite_sorting_list[item]).lower() in line.lower():
                            # If both the item and value are in the line, append 'okay_lib' with 1
                            okay_lib.append(1)
                        else:
                            # If the item is in the line, but the value is not, append with 0
                            okay_lib.append(0)
                if '&END_PHOTO' in line:
                    # Once you reach the end, check if all variables in 'okay_lib' are equal to 1, which would mean that
                    # all search parameters are fulfilled by that particular photo. If that is the case, the 'temp_lib'
                    # should be saved into 'saved_photo'
                    if all(x == 1 for x in okay_lib):
                        remove_variable = False
                    if not remove_variable:
                        saved_photo.append(temp_lib)
                    # Reset all variables and libraries again, for the next photo
                    remove_variable = True
                    temp_lib = []
                    okay_lib = []
            # For all photos that have been saved within 'saved_photo', sort the data from those photos
            # as in make them personal dictionaries again and create a Photo class based on the information
            for item in saved_photo:
                self.fav_data_sorting(item)

    def fav_data_sorting(self, list):
        temp_dict = {}
        # Remove all the "{", "}" and "'", so none of those symbols will be shown in the value
        for line in list:
            line = line.replace('{', '')
            line = line.replace('}', '')
            line = line.replace("'", "")
            # As long as the line =/= '&END_PHOTO', separate the classification from the value and strip '\n' from it
            if '&END_PHOTO' not in line:
                question_response = line.split(":", 1)
                question = question_response[0].strip()
                response = question_response[1].replace('\n', '').strip()
                # 'camera' and 'rover' are dictionaries in the database, so they require another separation
                if 'camera' in line or 'rover' in line:
                    temp_inner_dict = {}
                    # Separate everything based on the ',' , as those are individual classifications and values
                    inner_dict = line.split(",")
                    for items in inner_dict:
                        # Separate the classifications and values again....
                        inner_question_response = items.split(":", 1)
                        inner_question = inner_question_response[0].strip()
                        inner_response = inner_question_response[1].strip()
                        # If the inner_response still contains ':', it means it hasn't been separated properly
                        # Therefore, of course, more separation
                        if ':' in inner_response:
                            inner_question_response = items.split(":", 2)
                            inner_question = inner_question_response[1]
                            inner_response = inner_question_response[2]
                            # Save the classifications and values after all that separation, as a dictionary
                        temp_inner_dict[inner_question] = inner_response
                        # Save the dictionary as a response
                    response = temp_inner_dict
                    # Save everything as classifications and values, within the temp_dict
                temp_dict[str(question)] = response
            else:
                # Once you reach '&END_PHOTO', create a photo based on the temp_dict and append it to the ID_list
                photo = Photo(temp_dict)
                self.UI.var_data.id_list.append(photo)
                # Empty the temp_dict for another run
                temp_dict = {}

    def create_fav(self):
        photo = self.UI.current_photo
        # Request to create a name/description of the photo, to make retrieval easier from 'fav_data.txt'
        name = askstring('Favorite Name', 'What do you want to call the photo')
        showinfo('Saved', 'Favorite been saved as, {}'.format(name))
        photo.dict['favorite name'] = '{}'.format(name)
        # Write all the data you have in the photo dict to 'fav_data.txt'
        with open('fav_data.txt', 'a') as file:
            for item in photo.dict:
                file.write(f'{item} : {photo.dict[item]}\n')
            file.write(f"&END_PHOTO\n")

    def remove_fav(self):
        photo = self.UI.current_photo
        # Create a dict for lines in 'fav_data.txt',
        # set up remove variable and a list with the line numbers u want to remove
        starting_lines = []
        remove_var = False
        delete_line = []
        # Open 'fav_data.txt' as readable
        with open('fav_data.txt', 'r') as f:
            lines = f.readlines()
            for line_number, line in enumerate(lines):
                # Append lines
                starting_lines.append(line)
                # If the 'id' of the photo you want to remove is in the line, start removing the lines
                if str(photo.dict['id']) in line:
                    remove_var = True
                # If remove_var is active, add the line number to the delete_line list
                if remove_var:
                    delete_line.append(line_number)
                # If u reach '&END_PHOTO' and the variable is active,
                # deactivate remove_var
                if '&END_PHOTO' in line and remove_var:
                    remove_var = False

        # Start editing 'fav_data.txt'
        with open('fav_data.txt', 'w') as f:
            for line_number, line in enumerate(starting_lines):
                # As long as the line_number is not in delete_line, write the line into 'fav_data.txt' again
                if line_number in delete_line:
                    continue
                f.write(line)
