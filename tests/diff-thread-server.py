import sys
import threading
from fastapi import FastAPI
from fastapi.responses import FileResponse
from tkinter import *

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageTk
import asyncio
import tkinter as tk
from asyncio import CancelledError
from contextlib import suppress
import random

app = FastAPI()
# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace this with specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def one_url(url):
    """One task."""
    print(f'run one_url: {url}')  # for debug
    sec = random.randint(1, 8)
    await asyncio.sleep(sec)
    return "url: {}\tsec: {}".format(url, sec)


async def do_urls():
    """Creating and starting 10 tasks."""
    tasks = [one_url(url) for url in range(10)]
    completed, pending = await asyncio.wait(tasks)
    results = [task.result() for task in completed]
    print("\n".join(results))


def do_tasks(async_loop):
    """Button-Event-Handler starting the asyncio part."""
    asyncio.ensure_future(do_urls(), loop=async_loop)


def start(lang, root=None, async_loop=None):
    global mainwindow, canvas

    # root.resizable(width=True, height=True)
    root.iconbitmap("assets/icon.ico")
    root.title('tkinter asyncio demo')
    Button(master=root, text="Asyncio Tasks", command=lambda: do_tasks(async_loop)).pack()

    root.update_idletasks()


async def wait():
    try:
        tasks = asyncio.all_tasks(loop)
        print(f'========{tasks}')
        for task in tasks:
            try:
                # await asyncio.sleep(3600)
                cancel_ok = task.cancel()
                print(cancel_ok, task)
            except asyncio.exceptions.CancelledError:
                print("done")


    except RuntimeError as err:
        print('SIGINT or SIGTSTP raised')
        print("cleaning and exiting")
        sys.exit(1)


def quit_window(icon, item):
    global loop, fastapi_thread

    print('Shutdown icon')
    icon.stop()

    print('Shutdown server')
    server.should_exit = True
    server.force_exit = True
    asyncio.run_coroutine_threadsafe(server.shutdown(), loop)

    print('Shutdown root')
    root.quit()

    # print('Wait for server and loop to finish')
    # asyncio.run_coroutine_threadsafe(wait(), loop)

    print('Stop loop')
    # loop.stop()




def show_window(icon, item):
    icon.stop()
    root.after(0, root.deiconify)


def withdraw_window():
    root.withdraw()
    image = Image.open("assets/icon.ico")
    menu = (item("Quit", lambda icon, item: threading.Thread(target=quit_window, args=(icon, item)).start()),
            item("Show", show_window))
    icon = pystray.Icon("name", image, "title", menu)
    # icon.run_detached()
    icon.run()


def start_fastapi_server(loop):
    import uvicorn
    global server
    config = uvicorn.Config(app, loop=loop, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    try:
        loop.run_until_complete(server.serve())
    except KeyboardInterrupt:
        print("Received Ctrl+C. Stopping gracefully...")
        # Cancel all running tasks
        for task in asyncio.Task.all_tasks():
            task.cancel()
        # Optionally: Close any open resources (sockets, files, etc.)
        # Cleanup code here
    # finally:
    #     loop.close()


def start_tkinter_app(async_loop):
    global root, settings, db, canvas, locale
    root = tk.Tk()

    locale = 'en'
    start(locale, root, async_loop)

    root.protocol('WM_DELETE_WINDOW', withdraw_window)

    root.mainloop()


if __name__ == "__main__":
    global loop, fastapi_thread
    loop = None

    if sys.platform == "win32" and (3, 8, 0) <= sys.version_info < (3, 9, 0):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


    if sys.platform == 'win32':

        asyncio.get_event_loop().close()
        # On Windows, the default event loop is SelectorEventLoop, which does
        # not support subprocesses. ProactorEventLoop should be used instead.
        # Source: https://docs.python.org/3/library/asyncio-subprocess.html
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()

    # Start FastAPI server in a separate thread
    fastapi_thread = threading.Thread(target=start_fastapi_server, args=(loop,)).start()

    start_tkinter_app(loop)