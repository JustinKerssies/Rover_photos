"""
    File that creates a manifest button and what happens when manifest is initiated
"""

from tkinter import *
from _manifest_tab import Manifest_tab
from API import manifest_retrieval
from functions_import import print_entire_manifest, get_selected_name

class Manifest(Button):

    def __init__(self, UI=None, master=None):
        # save master and main UI for easy access
        super().__init__(master=master)
        self.master = master
        self.UI = UI
        master.update()
        master.pack_propagate(False)
        self.size = master.winfo_width(), master.winfo_height()
        # create button
        search_button = Button(master, text='manifest', command=self.clicked)
        search_button.pack(expand=True, fill='both')

    def clicked(self):
        # create a tab
        tab = Manifest_tab(self.master, self.size)
        if not tab.cancel:
            # if the tab wasn't cancelled
            self.UI.var_data.initialize()
            # get the name based on the radio button selected,
            # retrieve the data from manifest and print it in the terminal
            get_selected_name(self.UI.var_data, tab.rover.get())
            manifest_retrieval(self.UI.var_data)
            print_entire_manifest(self.UI.var_data)
        else:
            pass
        try:
            tab.manifest.destroy()
        except TclError:
            pass
