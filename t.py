# -*- coding: utf-8 -*-
"""20180912
学习 Frame 布局
bind 键盘事件
显示图片

使用:
     1. 创建多个frame 对象，frame = Frame(...)，没有指定master,默认当前Tk对象
     2  将各个frame 合适的布局在主面板上
     3  往各个frame添加子控件

涉及:
    Frame,Text,Button,PhotoImage,Label
    按钮动作函数、 bind 事件
"""
from tkinter import *
import time
import tkinter as tk

def msgsend():
    '''send按钮动作  发送消息，发送框内容消失，输出框内容显示

    1、在<消息列表分区>的文本控件中实时添加时间；
    2、获取<发送消息分区>的文本内容，添加到列表分区的文本中；
    3、将<发送消息分区>的文本内容清空。
    '''
    msg = '我'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+'\n'
    txt_msglist.insert(END, msg, 'green') # 表示 绿色字符插入到Text最后
    txt_msglist.insert(END, txt_msgsend.get('0.0', END)) # 获取发送消息，添加文本到消息列表
    txt_msgsend.delete('0.0', END) # 清空发送消息

# cancle按钮动作 取消消息发送
def cancel():
    txt_msgsend.delete('0.0', END) # 清空发送消息

# 绑定up键
def msgsendEvent(event):
    if event.keysym == 'Up':    # ↑按钮
        msgsend()

root = Tk()
root.title('聊天窗口')

'''创建分区'''
## 在主面板上划分区域
# 注意Frame 没有指定 master=tk，猜测没有指定就用当前的 Tk()
message_show_Frame = Frame(height = 200, width=300) # 创建<消息列表分区 >
message_send_Frame = Frame(height = 200, width=300) # 创建<发送消息分区 >
button_Frame = Frame(height=200, width=300)         # 创建<按钮分区>
pic_right_Frame = Frame(height=600, width=100)      # 创建<图片分区>

##  Frame在主控件上的布局
message_show_Frame.grid(row=0, column=0)
message_send_Frame.grid(row=0, column=1)
button_Frame.grid(row=1, column=0)
pic_right_Frame.grid(row=1, column=1, rowspan=3)


'''创建各个Frame中的控件'''
## 输出Text
# txt_msglist = Text(message_show_Frame)
# txt_msglist.tag_config('green', foreground='blue') # 创建标签，不懂
# txt_msglist.grid()



preferdessuffix = tk.StringVar()
l_preferdessuffix = tk.Label(message_show_Frame, text='xxxxxx')
l_preferdessuffix.grid(row=0, column=0, sticky=W)
e_preferdessuffix = tk.Entry(message_show_Frame, width=55, textvariable=preferdessuffix)
e_preferdessuffix.grid(row=0, column=1, sticky=W)




l_preferdessuffix1 = tk.Label(message_show_Frame, text='xxxxxx')
l_preferdessuffix1.grid(row=0, column=2, sticky=W)
e_preferdessuffix2 = tk.Entry(message_show_Frame, width=55, textvariable=preferdessuffix)
e_preferdessuffix2.grid(row=0, column=3, sticky=W)
## 输入框Text
txt_msgsend = Text(message_send_Frame)
txt_msgsend.bind('<KeyPress-Up>', msgsendEvent) # 绑定‘UP’键与消息发送。
txt_msgsend.grid()

## 发送按钮
button_send = Button(button_Frame, text='Send', command=msgsend)
button_send.grid(row=0, column=0, sticky=W)  # 在Frame f_floor上的布局设置

## 取消按钮
button_cancel1 = Button(button_Frame, text='Cancel', command=cancel)
button_cancel1.grid(row=0, column=1, sticky=W)


button_send1 = Button(button_Frame, text='Send', command=msgsend)
button_send1.grid(row=1, column=0, sticky=W)  # 在Frame f_floor上的布局设置

## 取消按钮
button_cancel2 = Button(button_Frame, text='Cancel', command=cancel)
button_cancel2.grid(row=1, column=1, sticky=W)


button_send2 = Button(button_Frame, text='Send', command=msgsend)
button_send2.grid(row=2, column=0, sticky=W)  # 在Frame f_floor上的布局设置

## 取消按钮
button_cancel3 = Button(button_Frame, text='Cancel', command=cancel)
button_cancel3.grid(row=2, column=3, sticky=W)


## 标签显示图片
photo = PhotoImage(file='./assets/images.png')
label = Label(pic_right_Frame, image=photo)
label.image = photo
label.grid()


root.mainloop()