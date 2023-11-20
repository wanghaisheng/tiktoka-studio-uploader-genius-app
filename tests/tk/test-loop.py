from tkinter import *
from tkinter import messagebox
import asyncio
import threading
import random

def _asyncio_thread(async_loop):
    async_loop.run_until_complete(do_urls())

def do_tasks(async_loop):
    """ Button-Event-Handler starting the asyncio part. """
    threading.Thread(target=_asyncio_thread, args=(async_loop,)).start()


async def one_url(url):
    """ One task. """
    sec = random.randint(1, 8)
    await asyncio.sleep(sec)
    return 'url: {}\tsec: {}'.format(url, sec)

async def do_urls():
    """ Creating and starting 10 tasks. """
    tasks = [one_url(url) for url in range(10)]
    completed, pending = await asyncio.wait(tasks)
    results = [task.result() for task in completed]
    print('\n'.join(results))

def do_freezed():
    messagebox.showinfo(message='Tkinter is reacting.')

def main(async_loop):
    root = Tk()
    Button(master=root, text='Asyncio Tasks', command= lambda:do_tasks(async_loop)).pack()
    Button(master=root, text='Freezed???', command=do_freezed).pack()
    root.mainloop()

if __name__ == '__main__':
    async_loop = asyncio.get_event_loop()
    main(async_loop)

