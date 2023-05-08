"""
    Creation of a calendar to much simpler select a date in the search tab
"""

from tkinter import Button, Tk
from tkcalendar import Calendar
from datetime import date, timedelta


class CreateCalender(object):

    def __init__(self, widget, data, possible_dates, width, height):
        # retrieve data like all the dates that were found in the manifest
        possible_dates = possible_dates
        rover = data.search['name']
        self.data = data
        self.date = None
        self.widget = widget
        self.start_date = data.start_and_end_date[rover][0]
        self.end_date = data.start_and_end_date[rover][1]
        self.redefine_days()
        self.ca = Tk()
        self.create_calendar(data, width, height)
        self.compare_dates(possible_dates)
        self.cal.grid(column=0, columnspan=3, row=0)
        # if a date has the tag 'empty', make it grey
        self.cal.tag_config('empty', background='grey', foreground='white')

        # create the buttons
        save_button = Button(self.ca, text='save', command=self.save_date)
        save_button.grid(column=0, row=1, sticky='nwse')
        x_button = Button(self.ca, text='x', command=self.exit, width=5)
        x_button.grid(column=1, row=1, sticky='nsew')
        delete_button = Button(self.ca, text='delete', command=self.delete_date)
        delete_button.grid(column=2, row=1, sticky='nesw')

        self.ca.mainloop()

    def save_date(self):
        self.date = self.cal.get_date()
        self.ca.quit()

    def delete_date(self):
        self.date = None
        self.ca.quit()

    def exit(self):
        if self.data.currently_selected_date:
            data = self.data.currently_selected_date
            self.date = f'{data[0]}-{data[1]}-{data[2]}'
        self.ca.quit()

    def compare_dates(self, possible_dates):
        # compare all the days between the start date and end date and if the day is not in the possible days,
        # add the tag 'empty' to it
        delta = self.end_date - self.start_date  # returns timedelta
        for i in range(delta.days + 1):
            day = self.start_date + timedelta(days=i)
            if str(day) not in possible_dates:
                self.cal.calevent_create(day, 'empty', 'empty')

    def redefine_days(self):
        # recreate the start_date and end_date as integers
        temp_date = self.start_date
        temp_split = temp_date.split('-', 2)
        self.start_date = date(int(temp_split[0]), int(temp_split[1]), int(temp_split[2]))
        temp_date = self.end_date
        temp_split = temp_date.split('-', 2)
        self.end_date = date(int(temp_split[0]), int(temp_split[1]), int(temp_split[2]))

    def create_calendar(self, data, width, height):
        # create a calendar on the location of the parent widget, with the height and width specified
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 30
        y += self.widget.winfo_rooty() + 20
        self.ca.geometry('%dx%d' % (width, height))
        self.ca.wm_overrideredirect(True)
        self.ca.wm_geometry("+%d+%d" % (x, y))
        # If there already was a date selected before, select that date, otherwise go to a random date
        if data.currently_selected_date:
            selected_date = data.currently_selected_date
        else:
            selected_date = [2014, 3, 14]
        self.cal = Calendar(self.ca, selectmode='day', year=int(selected_date[0]), month=int(selected_date[1]),
                            day=int(selected_date[2]), date_pattern='y-mm-dd', mindate=self.start_date,
                            maxdate=self.end_date)


def date_retrieval(widget, data, dates_list, width, height):
    # create a calendar
    widget = CreateCalender(widget=widget, possible_dates=dates_list, width=width, height=height, data=data)
    retrieved_date = widget.date
    if retrieved_date:
        # split the retrieved date and save it in data.py
        temp_split = retrieved_date.split('-', 2)
        data.currently_selected_date = []
        for item in temp_split:
            data.currently_selected_date.append(item)
    widget.ca.destroy()
    return retrieved_date
