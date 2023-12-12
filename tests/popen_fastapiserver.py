import sys
from tkinter import *
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageTk
import asyncio
import tkinter as tk
from asyncio import CancelledError
from contextlib import suppress
import random
from async_tkinter_loop import async_handler, async_mainloop
from typing import Optional
import platform
import time
import shlex, subprocess
from batchrunworker import BatchWorker
from string import ascii_uppercase
import threading

console_encoding = "utf-8"
uvicorn_subprocess=None
if platform.system() == "Windows":
    from ctypes import windll

    console_code_page = windll.kernel32.GetConsoleOutputCP()
    if console_code_page != 65001:
        console_encoding = f"cp{console_code_page}"



async def task(name: str):
    print(f"Task '{name}' is running...")
    if name=='A':
        print('task failed')
    else:
        print('task ok')
    await asyncio.sleep(3)  # Pretend to do something
TASK_NAMES = ascii_uppercase  # 26 fake tasks in total

async def do_tasks(BATCH_SIZE=3):
    tasks = [task(name) for name in TASK_NAMES]
    worker = BatchWorker(tasks,BATCH_SIZE=BATCH_SIZE)
    await worker.run()

def do_tasks_wrap(i=0):
    print('55555555555555',i)
    asyncio.run(do_tasks(BATCH_SIZE=i))
def start(lang, root=None):
    global mainwindow, canvas

    # root.resizable(width=True, height=True)
    root.iconbitmap("assets/icon.ico")
    root.title('tkinter asyncio demo')
    Button(master=root, text="Asyncio Tasks", command=lambda:threading.Thread(target=do_tasks_wrap, args=(5,)).start()).pack()


    Button(master=root, text="Start Server", command=lambda:threading.Thread(target=start_fastapi_server).start()).pack(side=tk.LEFT)

    Button(master=root, text="Stop Server", command=stop).pack(side=tk.LEFT)

    root.update_idletasks()


def quit_window(icon):

    print('Shutdown icon')
    icon.stop()

    print('Shutdown server')
    if uvicorn_subprocess is not None:
        uvicorn_subprocess.terminate() 
        time.sleep(0.5)
        done=uvicorn_subprocess.poll()
        if done==None:
            print(f'server shutdown error :{done}')

        else:
            print('server shutdown')
    else:
        print('server not started')
    print('Shutdown root')
    # https://github.com/insolor/async-tkinter-loop/issues/10
    root.quit()
    root.destroy()




def show_window(icon, item):
    icon.stop()
    root.after(0, root.deiconify)


def withdraw_window():
    root.withdraw()
    image = Image.open("assets/icon.ico")

    menu = (item("Quit", lambda icon:quit_window(icon)),
            item("Show", show_window))

    
    icon = pystray.Icon("name", image, "title", menu)
    icon.run()

# https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true

def start_fastapi_server():
    global uvicorn_subprocess
    uvicorn_command = ["uvicorn", "fastapiserver:app", "--host", "0.0.0.0", "--port", "8000"]
    uvicorn_subprocess = subprocess.Popen(uvicorn_command) 
    try:
        outs, errs = uvicorn_subprocess.communicate(timeout=15)
    except subprocess.TimeoutExpired:
        uvicorn_subprocess.kill()
        outs, errs = uvicorn_subprocess.communicate()


def stop():
    if uvicorn_subprocess is not None:
        uvicorn_subprocess.terminate() 
        time.sleep(0.5)
        done=uvicorn_subprocess.poll()
        if done==None:
            print(f'server shutdown error :{done}')

        else:
            print('server shutdown')

def start_tkinter_app():
    global root, settings, db, canvas, locale
    root = tk.Tk()

    locale = 'en'
    start(locale, root)

    root.protocol('WM_DELETE_WINDOW', withdraw_window)

    async_mainloop(root)




if __name__ == "__main__":
    start_tkinter_app()