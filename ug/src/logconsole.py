import os,queue,sys

import tkinter as tk
from tkinter import OptionMenu, filedialog,ttk,Message,Toplevel,messagebox
try:
    import tkinter.scrolledtext as ScrolledText
except ImportError:
    import Tkinter as tk # Python 2.x
    import ScrolledText
from log import logger,logging
import pyperclip as clip

class QueueHandler(logging.Handler):
    """Class to send logging records to a queue

    It can be used from different threads
    """

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):

        self.log_queue.put(record)
        


class ConsoleUi:
    """Poll messages from a logging queue and display them in a scrolled text widget"""

    def __init__(self, frame,root,row=0,column=0):
        self.frame = frame
        # Create a ScrolledText wdiget
        self.scrolled_text = ScrolledText.ScrolledText(frame, state='disabled')
        
        self.scrolled_text.bind_all("<Control-c>",self.copy)



        # Bind right-click event to show context menu
        # https://stackoverflow.com/questions/30668425/tkinter-right-click-popup-unresponsive-on-osx
        MAC_OS = False
        if sys.platform == 'darwin':
            MAC_OS = True
        if MAC_OS:
            self.scrolled_text.bind('<Button-2>', self.show_context_menu)
        else:
            self.scrolled_text.bind('<Button-3>', self.show_context_menu)        

        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="Clear All Text", command=self.clear_text)
            
        self.scrolled_text.grid(row=row, column=column, columnspan=2,sticky='nswe')
        self.scrolled_text.configure(font='TkFixedFont')
        self.scrolled_text.tag_config('INFO', foreground='black')
        self.scrolled_text.tag_config('DEBUG', foreground='gray')
        self.scrolled_text.tag_config('WARNING', foreground='orange')
        self.scrolled_text.tag_config('ERROR', foreground='red')
        self.scrolled_text.tag_config('CRITICAL', foreground='red', underline=1)
        # Create a logging handler using a queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(asctime)s: %(message)s')
        self.queue_handler.setFormatter(formatter)
        logger.addHandler(self.queue_handler)

        # Start polling messages from the queue
        self.frame.after(100, self.poll_log_queue)
    def clear_text(self):

        self.scrolled_text.configure(state='normal')  # Enable text widget
        self.scrolled_text.delete(1.0, tk.END)  # Delete all text
        self.scrolled_text.configure(state='disabled')  # Disable text widget again
    # Create a right-click context menu
    def show_context_menu(self,event):
        self.context_menu.post(event.x_root, event.y_root)


    def copy(self,event):
        try:
            string = event.widget.selection_get()
            clip.copy(string)
        except:
            pass
    def display(self, record):
        msg = self.queue_handler.format(record)
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(tk.END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state='disabled')
        # Autoscroll to the bottom
        self.scrolled_text.yview(tk.END)

    def poll_log_queue(self):
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.frame.after(100, self.poll_log_queue)

class TextHandler(logging.Handler):
    # This class allows you to log to a Tkinter Text or ScrolledText widget
    # Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text
        self.max_length = 250


    def emit(self, record):
        msg = self.format(record)
        if len(msg) > self.max_length:
            lines = []
            while len(msg) > self.max_length:
                lines.append(msg[:self.max_length])
                msg = msg[self.max_length:]
            lines.append(msg)
            msg= '\n'.join(lines)

        def append():
            self.text.configure(state='normal')
            self.text.insert(tk.END, msg + '\n')
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(tk.END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)