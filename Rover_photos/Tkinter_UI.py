"""
    This file is the main file. In here the main UI gets created and all other files gets initialized.
"""

from tkinter import *
from tkinter.ttk import Progressbar
from fraction import fraction as fr
from fraction import pb
from data import Settings
from search import Search
from manifest import Manifest
from saved import Saved
from Zoom import ZoomingImage
from API import show_image, manifest_retrieval
from functions_import import details_text_function, img_sizing, adapt_current_photo_id
from threading import Thread

global img


class UI:

    def __init__(self):
        # Setup base window and vars
        self.root = Tk()
        width, height = self.root.winfo_screenwidth(), self.root.winfo_screenheight() - 80
        self.root.state('zoomed')
        self.root.geometry('%dx%d' % (width, height))
        self.root.title('Rover Photos')
        self.root.propagate(False)
        # Retrieve data from 'data.py'
        self.var_data = Settings()
        # Set up var in which the current photo class, progressbar etc gets added for easier reference
        self.current_photo = None
        self.progressbar = None
        self.panel = None
        # Set up a list in which widgets get added for easier deleting
        self.widget_list = []
        self.labels_list = []
        self.frames = []

        # Set up the main frames, with proportions 10%, 80%, 10%
        self.start_bar = Frame(self.root, width=width, height=fr(height, 10))
        self.pic_frame = Frame(self.root, width=width, height=fr(height, 80))
        self.bottom_bar = Frame(self.root, width=width, height=fr(height, 10))
        self.start_bar.pack(side='top', expand=True, fill='both')
        self.pic_frame.pack(side='top', expand=True, fill='both')
        self.bottom_bar.pack(side='top', expand=True, fill='both')
        # Fill the main frames with everything thats needed
        self.init_UI(self.start_bar)
        self.init_pic_display(self.pic_frame)
        self.init_bottom_UI(self.bottom_bar)
        # Retrieve all the ID's that have been favorite
        self.create_saved_list()
        self.root.update()
        self.threading()
        self.root.mainloop()

    def init_UI(self, parent=None):
        # Update parent (so winfo can be used) and create frames in which buttons get created
        parent.update()
        width, height = parent.winfo_width(), parent.winfo_height()
        start_button_frame = Frame(parent, width=fr(width, 40), height=height)
        start_button_frame.pack(side='left', expand=True, fill='both')
        manifest_button_frame = Frame(parent, width=fr(width, 30), height=height)
        manifest_button_frame.pack(side='left', expand=True, fill='both')
        favorite_button_frame = Frame(parent, width=fr(width, 30), height=height)
        favorite_button_frame.pack(side='left', expand=True, fill='both')
        # Create custom Button classes based on the function
        self.search = Search(self, start_button_frame)
        self.manifest = Manifest(self, manifest_button_frame)
        self.saved = Saved(self, favorite_button_frame)

    def init_pic_display(self, parent=None):
        # Update parent (so winfo can be used) and create frames in which the picture and text get created
        parent.update()
        width, height = parent.winfo_width(), parent.winfo_height()
        self.picture_display = Frame(parent, width=fr(width, 60), height=height)
        self.picture_display.grid(row=0, column=0, sticky='nesw')
        self.information_display = Frame(parent, width=fr(width, 40))
        self.information_display.grid(row=0, column=1, sticky='nesw')
        # Disable propagate so the widgets don't resize based on the size of the picture displayed
        self.information_display.pack_propagate(False)

    def init_bottom_UI(self, parent=None):
        # Update parent (so winfo can be used) and create frames in which buttons and progressbar etc. get created
        parent.update()
        width, height = parent.winfo_width(), parent.winfo_height()
        self.favorite_display = Frame(parent, width=fr(width, 70) - 2, height=height - 2, highlightthickness=1,
                                      highlightbackground='black')
        self.favorite_display.grid(row=0, column=0, sticky='nesw')
        self.favorite_display.propagate(False)
        self.change_display = Frame(parent, width=fr(width, 30) - 2, height=height - 2, highlightthickness=1,
                                    highlightbackground='black')
        self.change_display.grid(row=0, column=1, sticky='nesw')
        self.change_display.propagate(False)
        # init the creation of the widgets within the bottom frames
        self.create_buttons_and_data(self.change_display, self.favorite_display)

    def create_buttons_and_data(self, parent1=None, parent2=None):
        # Create the buttons in the change display (previous, save/remove, next)
        parent2width, parent2height = parent2.winfo_width(), parent2.winfo_height()
        self.previous_button = Button(parent1, text='previous', command=self.previous_image)
        self.previous_button.pack(side='left', expand=True, fill='both')
        self.save_button = Button(parent1, text='save', command=self.saved.create_fav)
        self.save_button.pack(side='left', expand=True, fill='both')
        self.next_button = Button(parent1, text='next', command=self.next_image)
        self.next_button.pack(side='left', expand=True, fill='both')
        data = Frame(parent2)
        data.pack(side='top', anchor='n', expand=True, fill='both')
        bar_frame = Frame(parent2)
        bar_frame.pack(side='top', expand=True, fill='both')
        text_frame = Frame(parent2)
        text_frame.pack(side='top', expand=True, fill='both')
        # Create a place where the current size, current photo no' and the progressbar can be displayed
        self.current_size = Label(data)
        self.current_size.pack(side='left', anchor='ne', expand=True, fill='both')
        self.current_id = Label(data, text='')
        self.current_id.pack(side='right', anchor='nw', expand=True, fill='both')
        bar_frame = Frame(parent2, width=fr(parent2width, 80))
        bar_frame.pack(side='top', expand=True, fill='both')
        self.progressbar = Progressbar(bar_frame, length=1000)
        self.progressbar.pack(side='top', expand=True, fill='both')
        self.var_data.progressbar_loc = self.progressbar
        self.prog_text = Label(text_frame)
        self.prog_text.pack(side='top', expand=True, fill='both')
        self.var_data.progressbar_text = self.prog_text

    def previous_image(self):
        # go to the previous photo in the ID list
        pb(self.var_data, 'changing ID')
        self.current_photo = adapt_current_photo_id(self.var_data, 'previous')

        self.create_image_data()

    def next_image(self):
        # go to the next photo in the ID list
        pb(self.var_data, 'changing ID')
        self.current_photo = adapt_current_photo_id(self.var_data, 'next')
        self.create_image_data()

    def create_image_data(self, parent=None):

        pb(self.var_data, "downloading img")
        # Take the current ID and retrieve the class associated with it, save this as 'self.current_photo'
        self.current_photo = self.var_data.id_list[self.var_data.current_id]
        show_image(self.current_photo)
        pb(self.var_data, "resizing images")
        # img needs to be global, as it is defined within a function and Tkinter does not like that
        global img
        # Save all the old widgets
        # Use img_sizing to figure out the optimal size within the boundaries of the max_pic width and height
        # While preserving the exact same ratio
        resize_factor = img_sizing(self.var_data, self.picture_display, self.current_photo)
        pb(self.var_data, "creating canvas and zooming picture")
        # If there is no image yet, create a new img. Else change the details within the canvas
        if not self.panel:
            self.panel = ZoomingImage(self.var_data, self.picture_display, 'temp_photo.png',
                                      resize_factor, self.current_size)
            self.panel.grid(sticky='nesw')
            self.panel.update()
            self.panel.wheel()
        else:
            self.panel.init(self.var_data, resize_factor)
            self.panel.update()
            self.panel.wheel()

        # Sort the questions and responses into their own Dict, to more easily request them later
        details_text_function(self.current_photo)
        # Create both a question and a response frame
        for items in self.frames:
            items.destroy()
        self.question_frame = Frame(self.information_display)
        self.response_frame = Frame(self.information_display)
        self.response_frame.pack(side='right', expand=True, fill='both')
        self.question_frame.pack(side='right', expand=True, fill='both')
        self.response_frame.pack_propagate(False)
        self.question_frame.pack_propagate(False)
        self.frames.append(self.question_frame)
        self.frames.append(self.response_frame)
        # For every response in .responses create a label within the corresponding frame
        # With as text the question and response within the .responses and .questions dict
        pb(self.var_data, "Finishing")
        for items in self.labels_list:
            items.destroy()
        self.labels_list = []
        for i, response in enumerate(self.current_photo.responses):
            question = self.current_photo.questions[i]
            questions_label = Label(self.question_frame, text=question, background='lightgrey', justify='right',
                                    anchor='e')
            responses_label = Label(self.response_frame, text=response, justify='left', anchor='w')
            questions_label.pack(expand=True, anchor='e', fill='both')
            responses_label.pack(expand=True, anchor='w', fill='both')

        # Create a text ( d / MaxRange) where d is the current photo and MaxRange is the total amount of photos
        text = f'{self.var_data.current_id + 1} / {len(self.var_data.id_list)}'
        self.current_id.config(text=text)
        self.progressbar['value'] = 0
        if int(self.current_photo.dict['id']) in self.var_data.fav_list:
            self.save_button.config(text='remove', command=self.saved.remove_fav)
        else:
            self.save_button.config(text='save', command=self.saved.create_fav)

    def create_saved_list(self):
        self.saved.retrieve_fav_ids()

    def threading(self):
        t1 = Thread(target=self.downloading_manifest, daemon=True)
        t1.start()

    def downloading_manifest(self):
        # Retrieve all the manifests in the background
        manifest_retrieval(self.var_data, 'Curiosity')
        manifest_retrieval(self.var_data, 'Opportunity')
        manifest_retrieval(self.var_data, 'Spirit')
        return


if __name__ == '__main__':
    app = UI()
