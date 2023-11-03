import tkinter as tk
import webbrowser
from tkinter import OptionMenu, filedialog,ttk

app = tk.Tk()


def display_selected_item_index(event): 
   global so
   print('index of this item is: {}\n'.format(so.current()))

def OptionCallBack(*args):
    print(variable.get())
    print(so.current())

variable = tk.StringVar(app)
variable.set("Select From List1")
variable.trace('w', OptionCallBack)


so = ttk.Combobox(app, textvariable=variable)
so.config(values =('Tracing Upstream1', 'Tracing Downstream1','Find Path1'))
so.grid(row=1, column=4, sticky='E', padx=10)
so.bind("<<ComboboxSelected>>", display_selected_item_index)  




variable2 = tk.StringVar(app)
variable2.set("Select From List2")
variable2.trace('w', OptionCallBack)


so2 = ttk.Combobox(app, textvariable=variable2)
so2.config(values =('Tracing Upstream2', 'Tracing Downstream2','Find Path2'))
so2.grid(row=3, column=4, sticky='E', padx=10)

app.mainloop()