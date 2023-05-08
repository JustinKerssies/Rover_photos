"""
    Creation of a search tab that handles the inputs of the user and returns it to the Search class
"""

from tkinter import *
from rover_calendar import date_retrieval
from threading import Thread
from time import sleep
from functions_import import get_selected_name


class SearchTab:

    def __init__(self, master, size, data):
        # create a lotta places where data can be stored
        self.saved_sol = None
        self.calendar_init = False
        self.master = master
        self.data = {}
        self.cancel = True
        self.var_data = data
        self.size = size
        self.saved_date = None
        # Create a toplevel widget and force focus
        self.search_tab = Toplevel(highlightbackground='black', highlightthickness=1)
        self.search_tab.focus_force()
        self.rover = IntVar(value=1)
        self.camera_name = StringVar()
        # Init creation
        self.init_base_tab()
        self.create_input(parent=self.search_tab)
        self.create_buttons(parent=self.search_tab)
        self.threading()
        self.search_tab.mainloop()

    def init_base_tab(self):
        # make the search_tab width the same as the button and make the height 200
        self.search_tab.geometry('%dx%d' % (self.size[0], 200))
        self.search_tab.bbox()
        x = self.master.winfo_rootx()
        y = self.master.winfo_rooty()
        self.search_tab.wm_overrideredirect(True)
        self.search_tab.wm_geometry("+%d+%d" % (x, y))
        self.search_tab.bind('<FocusOut>', self.close_tab)

    def create_input(self, parent):
        """Sol input"""
        tab_frame = Frame(parent)
        tab_frame.pack(side='top', padx=10, pady=10, expand=True, fill='x', anchor='center')
        desc_frame = Frame(tab_frame)
        desc_frame.pack(side='left', anchor='w')
        input_frame = Frame(tab_frame)
        input_frame.pack(side='right', anchor='e', expand=True, fill='x')

        sol_desc = Label(desc_frame, text='Sol: ')
        sol_desc.pack(side='top')
        self.sol_input = Entry(input_frame)
        self.sol_input.pack(side='top', expand=True, fill='x')
        '''Date input'''
        date_desc = Label(desc_frame, text='Date: ')
        date_desc.pack(side='top')
        self.calendar_button = Button(input_frame, text='select date', command=self.calendar_date_retrieval)
        self.calendar_button.pack(side='top', expand=True, fill='x')
        '''Camera input'''
        camera_desc = Label(desc_frame, text='Camera')
        camera_desc.pack(side='top')
        temp_dict = self.var_data.camera_options
        self.camera_frame = Frame(input_frame)
        self.camera_frame.pack(side='top', expand=True, fill='x')
        self.camera_menu = OptionMenu(self.camera_frame, self.camera_name, *temp_dict)
        self.camera_menu.pack(side='top', expand=True, fill='x')
        '''Rover input'''
        rad_frame = Frame(parent)
        rad_frame.pack(side='top')
        rad1 = Radiobutton(rad_frame, text='Curiosity', value=1, variable=self.rover)
        rad2 = Radiobutton(rad_frame, text='Opportunity', value=2, variable=self.rover)
        rad3 = Radiobutton(rad_frame, text='Spirit', value=3, variable=self.rover)
        rad1.pack(side='left')
        rad2.pack(side='left', expand=True, fill='x', anchor='center')
        rad3.pack(side='right')

    def create_buttons(self, parent):
        # Create 2 buttons for starting the search and cancelling the search
        button_frame = Frame(parent, highlightthickness=1, highlightcolor='black')
        button_frame.pack(side='bottom', padx=10, pady=10, expand=True, fill='x')
        start_search_button = Button(button_frame, text='Start Search', command=self.return_data)
        start_search_button.pack(side='left', expand=True, fill='x')
        stop_search_button = Button(button_frame, text='Stop Search', command=self.destroy_tab)
        stop_search_button.pack(side='right', expand=True, fill='x')

    def return_data(self):
        self.search_tab.update()
        self.cancel = False
        # if anything has been selected, add said var to self.data, so it can be retrieved
        if self.sol_input and not self.sol_input == '':
            self.data['sol'] = self.sol_input.get()
        if self.saved_date:
            self.data['earth_date'] = self.saved_date
        for camera_name in self.var_data.camera_options_all:
            if self.camera_name.get() in camera_name:
                self.data['camera'] = self.camera_name.get()
        if self.rover.get() == 1:
            self.data['name'] = 'Curiosity'
        elif self.rover.get() == 2:
            self.data['name'] = 'Opportunity'
        elif self.rover.get() == 3:
            self.data['name'] = 'Spirit'
        self.close_tab()

    def calendar_date_retrieval(self):
        # Create a calendar
        self.calendar_init = True
        # Get selected name based on the selected radiobutton
        get_selected_name(self.var_data, self.rover.get())
        rover = self.var_data.search['name']
        date_list = self.var_data.possible_dates[rover]
        # create said calendar
        date = date_retrieval(self.calendar_button, self.var_data, date_list, 250, 212)
        # retrieve the date, change the text to the selected date
        self.saved_date = date
        self.calendar_button.config(text=date)
        # change the camera option based on the selected date
        self.change_camera_options_date()
        self.reset_search_menu()
        self.calendar_init = False

    def close_tab(self, event=None):
        if not self.calendar_init:
            self.search_tab.quit()

    def destroy_tab(self, event=None):
        if not self.calendar_init:
            self.search_tab.destroy()

    def threading(self):
        self.t1 = Thread(target=self.check_for_changes, daemon=True)
        self.t1.start()

    def check_for_changes(self):
        # constantly check whether the sol_input has been changed, if this happens:
        # change the camera options based on the current input
        while True:
            try:
                sleep(.1)
                get_selected_name(self.var_data, self.rover.get())
                if not self.sol_input.get() == self.saved_sol:
                    self.saved_sol = self.sol_input.get()
                    self.change_camera_options_sol()
                    self.reset_search_menu()
            except:
                return

    def change_camera_options_date(self):
        # start with 'empty'
        self.var_data.camera_options = ['Empty']
        rover = self.var_data.search['name']
        try:
            for i, items in enumerate(self.var_data.manifest[rover]['photo_manifest']['photos']):
                # for all the photos within the manifest, compare the date to the selected date
                date = self.var_data.manifest[rover]['photo_manifest']['photos'][i]['earth_date']
                try:
                    if date == self.saved_date:
                        # if the date is the same as the selected date,
                        # append the camera options with all the cameras on that particular date
                        for camera in self.var_data.manifest[rover]['photo_manifest']['photos'][i]['cameras']:
                            self.var_data.camera_options.append(camera)
                except ValueError:
                    continue
        except KeyError:
            return
        self.reset_search_menu()

    def change_camera_options_sol(self):
        # start with 'empty'
        self.var_data.camera_options = ['Empty']
        rover = self.var_data.search['name']
        try:
            for i, items in enumerate(self.var_data.manifest[rover]['photo_manifest']['photos']):
                # Compare all the sols in the manifest to the current input
                sol = self.var_data.manifest[rover]['photo_manifest']['photos'][i]['sol']
                try:
                    if int(sol) == int(self.saved_sol):
                        # If the sol == to the current input, append self.camera_options with all the cameras
                        # on that particular sol
                        for camera in self.var_data.manifest[rover]['photo_manifest']['photos'][i]['cameras']:
                            self.var_data.camera_options.append(camera)
                except ValueError:
                    continue
        except KeyError:
            return
        if len(self.var_data.camera_options) == 1:
            return True
        print(self.var_data.camera_options)
        self.reset_search_menu()

    def reset_search_menu(self, event=None):
        # Destroy the OptionMenu when you have clicked any of the RadioButtons
        # This is because different rovers have different camera's
        self.camera_menu.destroy()

        # Create a new OptionMenu, with the right library and in the camera_frame
        temp_dict = self.var_data.camera_options
        self.camera_menu = OptionMenu(self.camera_frame, self.camera_name, *temp_dict)
        self.camera_menu.pack(side='top', expand=True, fill='x')
        if len(self.var_data.camera_options) == 1:
            self.camera_name.set('specified sol/date does not exist')
        else:
            self.camera_name.set('insert camera option here')
