"""
    Creation of a saved tab that handles all the saved inputs and returns them to the Saved Class
"""

from tkinter import Toplevel, Button, IntVar, Label, Frame, Entry
from fraction import fraction as fr


class Saved_tab:

    def __init__(self, master, size):
        self.data = {}
        self.master = master
        self.size = size
        self.cancel = True
        self.rover = IntVar(value=1)
        self.saved_tab = Toplevel(highlightbackground='black', highlightthickness=1)
        self.init_base_tab()
        self.saved_tab_input = Frame(self.saved_tab)
        self.saved_tab_input.pack(side='top', expand=True, fill='both')
        self.saved_tab_output = Frame(self.saved_tab)
        self.saved_tab_output.pack(side='top', expand=True, fill='both')
        self.create_inputs(self.saved_tab_input)
        self.create_buttons(self.saved_tab_output)
        self.saved_tab_input.update()
        self.saved_tab.mainloop()

    def init_base_tab(self):
        self.saved_tab.geometry('%dx%d' % (self.size[0], 150))
        self.saved_tab.bbox()
        x = self.master.winfo_rootx()
        y = self.master.winfo_rooty()
        self.saved_tab.wm_overrideredirect(True)
        self.saved_tab.wm_geometry("+%d+%d" % (x, y))

    def create_inputs(self, parent):
        parent.pack_propagate(False)
        parent.update()
        width, height = parent.winfo_width(), parent.winfo_height()
        sol_frame = Frame(parent)
        sol_frame.pack(side='top', expand=True, fill='both')
        date_frame = Frame(parent)
        date_frame.pack(side='top', expand=True, fill='both')
        sol_text = Label(sol_frame, text='Sol:', width=fr(width, 4))
        sol_text.pack(side='left', anchor='w')
        self.sol_input = Entry(sol_frame)
        self.sol_input.pack(side='right', anchor='w', expand=True, fill='x')
        date_text = Label(date_frame, text='earth-date:', width=fr(width, 4))
        date_text.pack(side='left', anchor='w')
        self.date_input = Entry(date_frame)
        self.date_input.pack(side='right', anchor='e', expand=True, fill='x')


    def print(self):
        print(self.rover.get())

    def create_buttons(self, parent):
        create_manifest_button = Button(parent, text='start', command=self.searching)
        create_manifest_button.pack(side='left', expand=True, fill='x')
        cancel_manifest_button = Button(parent, text='cancel', command=self.close_window)
        cancel_manifest_button.pack(side='right', expand=True, fill='x')

    def searching(self):
        if self.sol_input:
            self.data['sol'] = self.sol_input.get()
        if self.date_input:
            self.data['date'] = self.date_input.get()
        self.cancel = False
        self.close_window()

    def close_window(self):
        self.saved_tab.quit()