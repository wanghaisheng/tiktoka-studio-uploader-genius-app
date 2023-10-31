
import tkinter as tk
from tkinter import OptionMenu, filedialog,ttk,Message,Toplevel,messagebox


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

# 信息消息框
def showinfomsg(message,title='hints',DURATION = 500,parent=None):
    # msg1 = messagebox.showinfo(title="消息提示", message=message)
    # messagebox.after(2000,msg1.destroy)
    # parent.focus_force()
    top = Toplevel(parent)
    top.title(title)
    center_window(top)    
    # Update the Toplevel window's width to adapt to the message width

    message_widget=Message(top, text=message, padx=120, pady=120)
    message_widget.pack()
    message_widget.update_idletasks()
    window_width = message_widget.winfo_reqwidth() + 40  # Add padding      
    top.geometry(f"{window_width}x200")  # You can adjust the height as needed      
    top.after(DURATION, top.destroy)


# 疑问消息框

def askquestionmsg(message):
    msg4 = messagebox.askquestion(title="询问确认", message=message)
    print(msg4)


def askokcancelmsg(message):
    msg5 = messagebox.askokcancel(title="确定或取消", message=message)
    print(msg5)


def askretrycancelmsg(message):
    msg6 = messagebox.askretrycancel(title="重试或取消", message=message)
    print(msg6)


def askyesonmsg(message):
    msg7 = messagebox.askyesno(title="是或否", message="是否开启团战")
    print(msg7)


def askyesnocancelmsg(message):
    msg8 = messagebox.askyesnocancel(title="是或否或取消", message="是否打大龙", default=messagebox.CANCEL)
    print(msg8)
    
def find_key(input_dict, value):
    if type(input_dict)==list:
        input_dict=dict(input_dict)
    result = "None"
    for key,val in input_dict.items():
        if val == value:
            result = key
    return result
