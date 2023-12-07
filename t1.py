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
from async_tkinter_loop import async_handler, async_mainloop

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


def do_tasks():
    """Button-Event-Handler starting the asyncio part."""
    asyncio.ensure_future(do_urls())


def start(lang, root=None):
    global mainwindow, canvas

    # root.resizable(width=True, height=True)
    root.iconbitmap("assets/icon.ico")
    root.title('tkinter asyncio demo')
    Button(master=root, text="Asyncio Tasks", command=async_handler(do_tasks())).pack()

    root.update_idletasks()


@async_handler
async def quit_window(icon):
    global loop, fastapi_thread

    print('Shutdown icon')
    icon.stop()

    print('Shutdown server')
    server.should_exit = True
    server.force_exit = True
    await server.shutdown()
    print('Shutdown root')
    root.quit()

    print('Stop loop')
    # loop.stop()




def show_window(icon, item):
    icon.stop()
    root.after(0, root.deiconify)


def withdraw_window():
    root.withdraw()
    image = Image.open("assets/icon.ico")
    # menu = (item("Quit", lambda icon, item: threading.Thread(target=quit_window, args=(icon, item)).start()),
    #         item("Show", show_window))
    menu = (item("Quit", lambda icon:quit_window(icon)),
            item("Show", show_window))

    
    icon = pystray.Icon("name", image, "title", menu)
    # icon.run_detached()
    icon.run()

@async_handler
async def start_fastapi_server(loop):
    import uvicorn
    global server
    config = uvicorn.Config(app, loop=loop, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await asyncio.wait(server.serve())



def start_tkinter_app():
    global root, settings, db, canvas, locale
    root = tk.Tk()

    locale = 'en'
    start(locale, root)

    root.protocol('WM_DELETE_WINDOW', withdraw_window)

    # root.mainloop()
    async_mainloop(root)




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
    # start_fastapi_server(loop)
    start_tkinter_app()