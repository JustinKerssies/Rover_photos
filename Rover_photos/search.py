"""
    Creation of a Search Button and holds all the functions that have to do with the main Search
"""

from tkinter import *
from _search_tab import SearchTab
from API import retrieve_id
from fraction import pb




class Search(Button):

    def __init__(self, UI=None, master=None):
        super().__init__(master=master)
        self.master = master
        self.UI = UI
        # Disable propagate to make sure it doesnt resize
        master.pack_propagate(False)
        master.update()
        self.size = master.winfo_width(), master.winfo_height()
        # Create Search Button and make sure it fills the entire master frame
        search_button = Button(master, text='search', command=self.clicked)
        search_button.pack(expand=True, fill='both')

    def clicked(self):
        # Retrieve the data.py that is used in the main file and save it as 'd'
        d = self.UI.var_data
        self.UI.progressbar['value'] = 0

        # Create a Search Tab in which you can fill in data
        self.tab = SearchTab(self.master, self.size, d)
        if self.tab.cancel:
            # If cancelled, don't do anything
            return
        pb(d, 'initializing')
        # Reset all variable data within data.py
        d.initialize()

        # Add all retrieved data to the search list in data.py
        for item in self.tab.data:
            if not self.tab.data[item] == '':
                d.search[item] = self.tab.data[item]
        try:
            self.tab.search_tab.destroy()
        except TclError:
            pass
        pb(d, "retrieving photo id's")
        empty = retrieve_id(self.UI.var_data)
        if empty:
            # If everything is empty, don't do anything
            return
        pb(d, "start creating image")
        self.UI.create_image_data()

