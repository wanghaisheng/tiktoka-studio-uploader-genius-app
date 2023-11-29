from pystray import MenuItem as item
import pystray
from PIL import Image
import tkinter as tk


def quit_window(icon, item):
    icon.stop()
    window.destroy()

def show_window(icon, item):
    icon.stop()
    window.after(0,window.deiconify)

def withdraw_window():  
    window.withdraw()
    image = Image.open("assets/icon.ico")
    menu = (item('Quit', quit_window), item('Show', show_window))
    icon = pystray.Icon("name", image, "title", menu)
    icon.run()




if __name__ == '__main__':
   global root
   window = tk.Tk()
   window.title("Welcome")
   
   window.protocol('WM_DELETE_WINDOW', withdraw_window)
   window.mainloop()


