#!/bin/env python3
import asyncio
import tkinter as tk
import random
from async_tkinter_loop import async_mainloop
from pystray import MenuItem as item
import pystray
from PIL import Image

import threading
from fastapi import FastAPI
from fastapi.responses import FileResponse
from tkinter import *

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
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

    i = 0
    while True:
        await event.wait()
        i += 1
        # """Creating and starting 10 tasks."""
        # tasks = [one_url(url) for url in range(10)]
        # completed, pending = await asyncio.wait(tasks)
        # results = [task.result() for task in completed]
        # print("\n".join(results))
        await one_url(i)
        await asyncio.sleep(1.0)




async def counter(loop):
    i = 0
    if True:
        await event.wait()
        import uvicorn
        global server
        config = uvicorn.Config(app, loop=loop, host="0.0.0.0", port=8000)
        server = uvicorn.Server(config)
        try:

            await server.serve()
            await asyncio.sleep(1.0)
        except KeyboardInterrupt:
            print("Received Ctrl+C. Stopping gracefully...")
            # Cancel all running tasks
            for task in asyncio.Task.all_tasks():
                task.cancel()
    else:
        await server.shutdown()

root = tk.Tk()

label = tk.Label(root)
label.pack()

def quit_window(icon, item):
    global loop, fastapi_thread

    
    print('Shutdown icon')
    icon.stop()

    print('Shutdown server')
    # server.should_exit = True
    # server.force_exit = True
    # asyncio.run_coroutine_threadsafe(server.shutdown(), loop)

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
    menu = (item("Quit", quit_window(icon)),
            item("Show", show_window))
    icon = pystray.Icon("name", image, "title", menu)
    # icon.run_detached()
    icon.run()


def start_stop():
    if event.is_set():
        event.clear()
    else:
        event.set()

root.protocol('WM_DELETE_WINDOW', withdraw_window)

tk.Button(root, text="Start/stop", command=start_stop).pack()

event = asyncio.Event()

# Start background task
loop=asyncio.get_event_loop_policy().get_event_loop()
loop.create_task(counter(loop))

async_mainloop(root)