from tkinter import *
import os
import sys

class ScrollableList(Frame):

    def __init__(self, parent, vscroll=True, hscroll=False):
        Frame.__init__(self, parent)
        self.grid(sticky=NSEW)        
        if vscroll:
            self.vScrollbar = Scrollbar(self, orient=VERTICAL)
            self.vScrollbar.grid(row=0, column=1, sticky=N+S)
        if hscroll:
            self.hScrollbar = Scrollbar(self, orient=HORIZONTAL)
            self.hScrollbar.grid(row=1, column=0, sticky=E+W)
        self.listbox = Listbox(self, selectmode=SINGLE)
        self.listbox.grid(row=0, column=0,sticky='nswe')
        if vscroll:
            self.listbox['yscrollcommand'] = self.vScrollbar.set
            self.vScrollbar['command'] = self.listbox.yview
        if hscroll:
            self.listbox['xscrollcommand'] = self.hScrollbar.set
            self.hScrollbar['command'] = self.listbox.xview
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)

class Application(Frame):

    @classmethod
    def main(cls):
        NoDefaultRoot()
        root = Tk()
        app = cls(root)
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        root.resizable(True, True)
        root.mainloop()

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.grid(sticky=NSEW)
        options = dict(sticky=NSEW, padx=3, pady=4)
        self.list1 = ScrollableList(self)
        # self.list2 = ScrollableList(self)
        self.list1.grid(row=0, column=0, **options)
        # self.list2.grid(row=0, column=1, **options)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

if __name__ == "__main__":
    Application.main()
