# --- class ---

import calendar
import tkinter

class TkinterCalendar(calendar.Calendar):

    def formatmonth(self, master, year, month):

        dates = self.monthdatescalendar(year, month)

        frame = tkinter.Frame(master)

        self.labels = []

        for r, week in enumerate(dates):
            labels_row = []
            for c, date in enumerate(week):
                label = tkinter.Button(frame, text=date.strftime('%Y\n%m\n%d'))
                label.grid(row=r, column=c)

                if date.month != month:
                    label['bg'] = '#aaa'

                if c == 6:
                    label['fg'] = 'red'

                labels_row.append(label)
            self.labels.append(labels_row)

        return frame


# --- example how to use ---

import tkinter as tk

root = tk.Tk()

tkcalendar = TkinterCalendar()

for year, month in [(2017, 11), (2017, 12), (2018,1)]:
    tk.Label(root, text = '{} / {}'.format(year, month)).pack()

    frame = tkcalendar.formatmonth(root, year, month)
    frame.pack()

root.mainloop()                                      