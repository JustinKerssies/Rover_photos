"""
    Creates Tab for the Manifest Button
"""

from tkinter import Toplevel, Button, IntVar, Radiobutton, Frame


class Manifest_tab:

    def __init__(self, master, size):
        # Create a toplevel frame with 3 radiobuttons and 2 normal buttons
        # The radiobuttons represent the rovers, while the normal buttons either print the manifest or cancel it
        self.master = master
        self.size = size
        self.cancel = True
        self.rover = IntVar(value=1)
        self.manifest = Toplevel(highlightbackground='black', highlightthickness=1)
        self.manifest_input = Frame(self.manifest)
        self.manifest_input.pack(side='top', expand=True, fill='both')
        self.manifest_output = Frame(self.manifest)
        self.manifest_output.pack(side='top', expand=True, fill='both')
        self.init_base_tab()
        self.create_radio_buttons()
        self.create_buttons()
        self.manifest.mainloop()

    def init_base_tab(self):
        self.manifest.geometry('%dx%d' % (self.size[0], 200))
        self.manifest.bbox()
        x = self.master.winfo_rootx()
        y = self.master.winfo_rooty()
        self.manifest.wm_overrideredirect(True)
        self.manifest.wm_geometry("+%d+%d" % (x, y))

    def create_radio_buttons(self):
        rad1 = Radiobutton(self.manifest_input, text='Curiosity', value=1, variable=self.rover)
        rad2 = Radiobutton(self.manifest_input, text='Opportunity', value=2, variable=self.rover)
        rad3 = Radiobutton(self.manifest_input, text='Spirit', value=3, variable=self.rover)
        rad1.pack(side='left')
        rad2.pack(side='left', expand=True, fill='x', anchor='center')
        rad3.pack(side='right')

    def create_buttons(self):
        create_manifest_button = Button(self.manifest_output, text='print manifest', command=self.return_rover)
        create_manifest_button.pack(side='left', expand=True, fill='x')
        cancel_manifest_button = Button(self.manifest_output, text='cancel manifest', command=self.close_window)
        cancel_manifest_button.pack(side='right', expand=True, fill='x')

    def return_rover(self):
        self.cancel = False
        self.close_window()

    def close_window(self):
        self.manifest.quit()
