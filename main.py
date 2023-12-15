import sys
from threading import Thread
from time import sleep

import requests
# import webview

from uploadergenius.license import validate_or_remove_license
from uploadergenius.log import logger
from uploadergenius.server.app import boot, server

from uploadergenius.settings import get_window_settings
from uploadergenius.settings.constants import DEBUG, GUI_LIB, SERVER_HOST
from uploadergenius.version import get_version
from uploadergenius.window import     start_tkinter_app,quit_window

import asyncio

def run_cache_cleanup_later():
    sleep(120)  # TODO: make this more intelligent?



def run_server():
    logger.debug(f"Starting server on {SERVER_HOST}:{server.get_port()}")

    try:
        server.serve()
    except Exception as e:
        logger.exception(f"Exception in server thread!: {e}")



def monitor_server(server):
    while True:
        if not server.is_alive():
            logger.critical(f"Thread: {thread} died, exiting!")
            quit_window(icon=None)
            server.shutdown()
            sys.exit(2)
        else:
            sleep(0.5)



def monitor_threads(*threads):
    while True:
        for thread in threads:
            if not thread.is_alive():
                logger.critical(f"Thread: {thread} died, exiting!")
                quit_window(icon=None)
                server.stop()
                sys.exit(2)
        else:
            sleep(0.5)


def run_thread(target):
    def wrapper(thread_name):
        try:
            target()
        except Exception as e:
            logger.exception(f"Unexpected exception in thread {thread_name}!: {e}")

    thread = Thread(
        target=wrapper,
        args=(target.__name__,),
    )
    thread.daemon = True
    thread.start()


def main():
    logger.info(f"\n#\n# Booting UploaderGenius {get_version()}\n#")

    boot()
    print('start server thread')
    # server_thread = Thread(name="Server", target=run_server)
    # # server_thread.daemon = True
    # server_thread.start()

    # run_thread(validate_or_remove_license)
    # run_thread(run_cache_cleanup_later)
    print('test server works')
    print(f'import start server {server.host}:{server.port}')

    # Ensure the webserver is up & running by polling it
    waits = 0
    while waits < 10:
        try:
            response = requests.get(f"http://{server.host}:{server.port}/static/index.html")
            print('server response',response.status_code)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.warning(f"Waiting for main window: {e}")
            sleep(0.1 * waits)
            waits += 1
        else:
            break
    else:
        logger.critical("Webserver did not start properly!")
        sys.exit(2)

    # create_window(
    #     unique_key="main",
    #     **get_window_settings(),
    # )
    # Let's hope this thread doesn't fail!
    # monitor_thread = Thread(
    #     name="Thread monitor",
    #     target=monitor_threads,
    #     args=(server_thread,),
    # )
    # monitor_thread.daemon = True
    # monitor_thread.start()

    if DEBUG:
        sleep(1)  # give webpack a second to start listening

    # Start the GUI - this will block until the main window is destroyed

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

    start_tkinter_app(loop=None)

    logger.debug("Main window closed, shutting down...")
    server.shutdown()
    sys.exit()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        server.shutdown()
        raise