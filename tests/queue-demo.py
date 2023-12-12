#!/usr/bin/python3
import sys
import threading
import queue
import datetime
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Clock(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.queue = queue.Queue()
        self.check = True

    def stop(self):
        self.check = False

    def run(self):

        """Feeds the tail."""

        while self.check:
            s = "Astral date: "
            t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            msg = "{0} {1}".format(s, t)
            time.sleep(1)
            self.queue.put(msg)
    
    def check_queue(self, obj):

        """Returns a formatted string representing time.
           obj in this case is the statusbar text"""

        while self.queue.qsize():
            try:
                x = self.queue.get(0)
                msg = "{0}".format(x)
                obj.set(msg)
            except queue.Empty:
                pass
            

class Main(ttk.Frame):
    def __init__(self, parent, ):
        super().__init__(name="main")

        self.parent = parent
        self.text = tk.StringVar()
        self.spins = tk.IntVar()
        self.option = tk.IntVar()
        self.check = tk.BooleanVar()
        self.values = ('Apple','Banana','Orange')
        self.status_bar_text = tk.StringVar()
        self.init_status_bar()
        self.init_ui()

    def init_status_bar(self):

        self.status = tk.Label(self,
                               textvariable=self.status_bar_text,
                               bd=1,
                               relief=tk.SUNKEN,
                               anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)        
          
    def init_ui(self):

        f0 = ttk.Frame(self)
        f1 = ttk.Frame(f0,)

        ttk.Label(f1, text = "Combobox").pack()
        self.cbCombo = ttk.Combobox(f1,state='readonly',values=self.values)
        self.cbCombo.pack()
        
        ttk.Label(f1, text = "Entry").pack()
        self.txTest = ttk.Entry(f1, textvariable=self.text).pack()

        ttk.Label(f1, text = "Spinbox").pack()
        tk.Spinbox(f1, from_=0, to=15, textvariable= self.spins).pack()

        ttk.Label(f1, text="Checkbutton:").pack()
        ttk.Checkbutton(f1,
                       onvalue=1,
                       offvalue=0,
                       variable=self.check).pack()


        ttk.Label(f1, text="Radiobutton:").pack()
        for index, text in enumerate(self.values):
            ttk.Radiobutton(f1,
                            text=text,
                            variable=self.option,
                            value=index,).pack()
            

        ttk.Label(f1, text="Listbox:").pack()
        self.ListBox = tk.Listbox(f1)
        self.ListBox.pack()
        self.ListBox.bind("<<ListboxSelect>>", self.on_listbox_select)
        self.ListBox.bind("<Double-Button-1>", self.on_listbox_double_button)
        
              
        f2 = ttk.Frame(f0,)

        bts = [("Callback", 7, self.on_callback, "<Alt-k>"),
               ("Args", 0, self.on_args, "<Alt-a>"),
               ("kwargs", 1, self.on_kwargs, "<Alt-w>"),
               ("Set", 0, self.on_set, "<Alt-s>"),
               ("Reset", 0, self.on_reset, "<Alt-r>"),
               ("Close", 0, self.on_close, "<Alt-c>")]

        for btn in bts:
            ttk.Button(f2,
                       text=btn[0],
                       underline=btn[1],
                       command = btn[2]).pack(fill=tk.X, padx=5, pady=5)
            self.parent.bind(btn[3], btn[2])
            
        f1.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        f2.pack(side=tk.RIGHT, fill=tk.Y, expand=0)
        f0.pack(fill=tk.BOTH, expand=1)

    def on_open(self):
        self.periodic_call()
        
    def on_callback(self, evt=None):

        print ("self.cbCombo = {}".format(self.cbCombo.get()))
        print ("self.text = {}".format(self.text.get()))
        print ("self.spins = {}".format(self.spins.get()))
        print ("self.check = {}".format(self.check.get()))
        print ("self.option = {}".format(self.option.get()))
        if self.ListBox.curselection():
            print("ListBox.curselection = {}".format(self.ListBox.curselection()[0]))
        else:
            print("{0}".format("No selected item on listbox"))

    def on_args(self, evt=None):

        print("args type: {}".format(type(self.master.args)))
        for p, i in enumerate(self.master.args):
            print(p, i)

    def on_kwargs(self, evt=None):

        print("kwargs type: {}".format(type(self.master.kwargs)))
        for k, v in self.master.kwargs.items():
            print("{0}:{1}".format(k,v))

    def on_reset(self, evt=None):
        self.text.set('')
        self.spins.set(0)
        self.check.set(0)

    def on_set(self, evt=None):
        self.cbCombo.current(1)
        self.text.set('qwerty')
        self.spins.set(42)
        self.check.set(1)
        self.option.set(1)
        self.ListBox.delete(0, tk.END)
        
        for i in self.values:
            s = "{0}".format(i,)
            self.ListBox.insert(tk.END, s)
     
        self.ListBox.selection_set(1)

    def on_listbox_select(self, evt=None):

        if self.ListBox.curselection():

            index = self.ListBox.curselection()
            s = self.ListBox.get(index[0])
            print("on_listbox_select: index = {0} values = {1}".format(index, s))

    def on_listbox_double_button(self, evt=None):

        if self.ListBox.curselection():
            index = self.ListBox.curselection()
            s = self.ListBox.get(index[0])
            print("on_listbox_double_button: index = {0} values = {1}".format(index, s))

    def periodic_call(self):
        """This funciont check the data returned from the clock class queue."""

        self.parent.clock.check_queue(self.status_bar_text)
        
        if self.parent.clock.is_alive():
            self.after(1, self.periodic_call)
        else:
            pass                    
        
    def on_close(self, evt=None):
        self.parent.on_exit()


class App(tk.Tk):
    """Main Application start here"""
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.args = args
        self.kwargs = kwargs
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.set_style(kwargs["style"])  
        self.set_title(kwargs["title"])
        self.resizable(width=False, height=False)

        #start clock on a separate thread...
        self.set_clock()
        
        w = Main(self)
        w.on_open()
        w.pack(fill=tk.BOTH, expand=1)

    def set_clock(self,):
        self.clock = self.get_clock()
        self.clock.start()
        
    def get_clock(self,):
        """Instance the clock."""
        return Clock()
    
    def set_style(self, which):
        self.style = ttk.Style()
        self.style.theme_use(which)
        
    def set_title(self, title):
        s = "{0}".format(title)
        self.title(s)
        
    def on_exit(self):
        """Close all"""
        msg = "Do you want to quit?"
        if messagebox.askokcancel(self.title(), msg, parent=self):
            #stop the thread
            if self.clock is not None:
                self.clock.stop()
            self.destroy()

def main():

    args = []

    for i in sys.argv:
        args.append(i)

    #('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
    kwargs = {"style":"clam", "title":"Simple App",}

    app = App(*args, **kwargs)

    app.mainloop()

if __name__ == '__main__':
    main()            
    