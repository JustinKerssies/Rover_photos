"""
    Class with a zooming image
"""

from tkinter import *
from PIL import Image, ImageTk



class AutoScrollbar(Scrollbar):
    ''' A scrollbar that hides itself if it's not needed.
        Works only if you use the grid geometry manager '''

    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise TclError('Cannot use pack with this widget')

    def place(self, **kw):
        raise TclError('Cannot use place with this widget')


class ZoomingImage(Frame):

    def __init__(self, data, frame, path, resize_factor, adaptable_widget):
        # Setup base settings
        Frame.__init__(self, master=frame)
        self.master.update()
        width, height = self.master.winfo_width(), self.master.winfo_height()
        self.big_frame = Frame(self.master, width=width, height=height)
        self.big_frame.grid(sticky='nsew')
        self.master.grid_propagate(False)
        self.current_size = adaptable_widget
        self.path = path
        self.data = data
        self.resize_factor = resize_factor
        self.canvas_middle = width / 2, height / 2
        # Add scrollbars that disappear when not used
        vbar = AutoScrollbar(self.master, orient='vertical')
        hbar = AutoScrollbar(self.master, orient='horizontal')
        vbar.grid(row=0, column=1, sticky='ns')
        hbar.grid(row=1, column=0, sticky='we')
        self.resize_factor = resize_factor
        self.image = Image.open('temp_photo.png')
        self.canvas = Canvas(self.big_frame, xscrollcommand=hbar.set, yscrollcommand=vbar.set,
                             width=width, height=height)
        self.canvas.grid(row=0, column=0, sticky='ensw')
        self.canvas.grid_propagate(False)
        vbar.configure(command=self.canvas.yview)  # bind scrollbars to the canvas
        hbar.configure(command=self.canvas.xview)

        self.canvas.bind('<ButtonPress-1>', self.move_from)
        self.canvas.bind('<B1-Motion>', self.move_to)
        self.canvas.bind('<MouseWheel>', self.wheel)

        # Create place for image and retrieve vars in data.py
        self.imageid = None
        self.delta = data.zoom_delta
        self.imscale = resize_factor * self.delta

        # Add text to use as reference
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        self.text = self.canvas.create_text(0, 0, anchor='center', justify='left')
        self.canvas.update()

    def init(self, data, resize_factor):
        # Reinit the canvas when the image has changed
        if self.imageid:
            self.canvas.delete(self.imageid)
            self.imageid = None
            self.canvas.imagetk = None
        self.image = Image.open('temp_photo.png')
        self.delta = data.zoom_delta
        self.imscale = resize_factor * self.delta
        self.data = data
        self.resize_factor = resize_factor
        self.canvas.moveto(self.text, 0, 0)

    def move_from(self, event=None):
        ''' Remember previous coordinates for scrolling with the mouse '''
        try:
            self.canvas.scan_mark(event.x, event.y)
        except AttributeError:
            self.canvas.scan_mark(0, 0)

    def move_to(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def wheel(self, event=None):
        ''' Zoom with mouse wheel '''

        scale = 1
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        try:
            if event.num == 5 or event.delta == -120:
                if self.imscale == self.resize_factor:
                    return
                scale *= self.delta
                self.imscale *= self.delta
                if self.imscale < self.resize_factor:
                    # Cant zoom out more than what it takes to fill the entire frame
                    current_scale = '%.4f' % self.imscale
                    delta = self.resize_factor - float(current_scale)
                    try:
                        scale /= delta
                    except ZeroDivisionError:
                        scale /= 1
                    self.imscale = self.resize_factor

            elif event.num == 4 or event.delta == 120:
                if self.imscale == self.data.max_zoom:
                    return
                scale /= self.delta
                self.imscale /= self.delta
                if self.imscale > self.data.max_zoom:
                    # Cant zoom in more than the max_zoom in data.py
                    delta = self.imscale - self.data.max_zoom
                    if not delta == 0:
                        scale *= delta
                    else:
                        scale *= 1
                    self.imscale = self.data.max_zoom

            # Rescale all canvas objects
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)
            self.canvas.scale('all', x, y, scale, scale)
            self.show_image()
            self.canvas.configure(scrollregion=self.canvas.bbox('all'))
            size = '%.4f' % self.imscale
            self.current_size.config(text=f'{size}x')
        except AttributeError:
            x, y = 0, 0
            scale /= self.delta
            self.imscale /= self.delta
            self.canvas.scale('all', x, y, scale, scale)
            self.show_image()
            self.canvas.configure(scrollregion=self.canvas.bbox('all'))

            size = '%.4f' % self.imscale
            self.current_size.config(text=f'{size}x')

    def show_image(self, init=None):
        ''' Show image on the Canvas '''
        if self.imageid:
            self.canvas.delete(self.imageid)
            self.imageid = None
            self.canvas.imagetk = None  # delete previous image from the canvas
        width, height = self.image.size
        new_size = int(self.imscale * width), int(self.imscale * height)
        imagetk = ImageTk.PhotoImage(self.image.resize(new_size))
        # Use self.text object to set proper coordinates
        self.imageid = self.canvas.create_image(self.canvas.coords(self.text), image=imagetk)
        self.canvas.lower(self.imageid)  # set it into background
        self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection
