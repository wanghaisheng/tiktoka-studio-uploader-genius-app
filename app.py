import tkinter as tk
from tkinter import ttk
from main  import render,load_setting
class Win(tk.Frame):
    """
    Displays a series of buttons that change the colour of the Tkinter 
    frame when pressed.
    """
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        load_setting()
        self.lang=render(master,'zh')
root = tk.Tk()
# root.geometry('1280x720')
window_size='750x540'

root.geometry(window_size)
root.title('youtube 视频批量上传助手测试版')        

root.resizable(width=False, height=False)
root.iconbitmap("assets/icon.ico")
root.update()
defaultlang='zh'
app = Win(root)
app.lang=defaultlang
prev_lang=app.lang
root.mainloop()