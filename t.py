#Create Scrolled Text widget in Python GUI Application  
import tkinter as tk  
from tkinter import ttk  
from tkinter import scrolledtext  
win = tk.Tk()  
win.title("Python GUI App")  
ttk.Label(win, text="This is Scrolled Text Area").grid(column=0,row=0)  
#Create Scrolled Text  
scrolW=30  
scrolH=2  
scr=scrolledtext.ScrolledText(win, width=scrolW, height=scrolH, wrap=tk.WORD)  
scr.grid(column=0, columnspan=3)  
#Calling Main()  
win.mainloop()  