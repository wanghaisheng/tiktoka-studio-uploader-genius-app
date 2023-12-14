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
from asyncio.subprocess import Process
from typing import Optional
import platform

uvicorn_subprocess: Optional[Process] = None


console_encoding = "utf-8"

if platform.system() == "Windows":
    from ctypes import windll

    console_code_page = windll.kernel32.GetConsoleOutputCP()
    if console_code_page != 65001:
        console_encoding = f"cp{console_code_page}"



async def one_url(url):
    """One task."""
    print(f'run one_url: {url}')  # for debug
    sec = random.randint(1, 8)
    await asyncio.sleep(sec)
    return "url: {}\tsec: {}".format(url, sec)


async def do_urls(i=10):
    """Creating and starting 10 tasks."""
    tasks = [one_url(url) for url in range(i)]
    completed, pending = await asyncio.wait(tasks)
    results = [task.result() for task in completed]
    print("\n".join(results))

async def do_task():
    print('get variable value')
    platform_value=platform_var.get()
    await do_urls(i=platform_value)
def start(lang, root=None):
    global mainwindow, canvas

    # root.resizable(width=True, height=True)
    root.iconbitmap("assets/icon.ico")
    root.title('tkinter asyncio demo')
    global platform_var
    platform_var = tk.IntVar()
    platform_var.set(5)
    Button(master=root, text="Asyncio Tasks", command=async_handler(do_task)).pack()
    Button(master=root, text="Start Server", command=start_fastapi_server).pack(side=tk.LEFT)

    Button(master=root, text="Stop Server", command=stop).pack(side=tk.LEFT)

    root.update_idletasks()


def quit_window(icon):

    print('Shutdown icon')
    icon.stop()

    print('Shutdown server')
    if uvicorn_subprocess is not None:
        uvicorn_subprocess.kill()
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


@async_handler
async def start_fastapi_server():
    global uvicorn_subprocess
    uvicorn_command = ["uvicorn", "fastapiserver:app", "--host", "0.0.0.0", "--port", "8000"]

    uvicorn_subprocess = await asyncio.create_subprocess_exec(
        *uvicorn_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    while uvicorn_subprocess.returncode is None:
        stdout = asyncio.create_task(uvicorn_subprocess.stdout.readline())
        stderr = asyncio.create_task(uvicorn_subprocess.stderr.readline())

        done, pending = await asyncio.wait({stdout, stderr}, return_when=asyncio.FIRST_COMPLETED)

        if stdout in done:
            result_text = stdout.result().decode(console_encoding)
            print(f'stdout:{result_text}')

        if stderr in done:
            result_text = stderr.result().decode(console_encoding)
            print(f'stderr:{result_text}')

        for item in pending:
            item.cancel()

    uvicorn_subprocess = None
def stop():
    if uvicorn_subprocess is not None:
        uvicorn_subprocess.kill()



def start_tkinter_app():
    global root, settings, db, canvas, locale
    root = tk.Tk()

    locale = 'en'
    start(locale, root)

    root.protocol('WM_DELETE_WINDOW', withdraw_window)

    async_mainloop(root)




if __name__ == "__main__":
    start_tkinter_app()