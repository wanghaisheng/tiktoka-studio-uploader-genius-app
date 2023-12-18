import asyncio
import concurrent.futures
import threading

class MyApp:
    def __init__(self) -> None:
        self.task: concurrent.futures.Future[int]|None = None

        self.task_event = asyncio.Event()
        self.task_event.clear()

    # An asyncio task that runs in the specified event loop
    async def process_task(self) -> int:
        try:
            self.task_event.clear()
            print("asyncio task is running")
            await asyncio.sleep(10)
            print("asyncio task is finished")
            return 123
        except asyncio.CancelledError:
            print("asyncio task is cancelled; rethrowing...")
            raise
        finally:
            print("Setting the asyncio task event")
            self.task_event.set()

    # Called immediately from task.cancel(), before the underlying
    # asyncio task completes.
    def task_done(self, future: concurrent.futures.Future[int]) -> None:
        if future.cancelled():
            print("Task cancelled (callback)")
        elif future.exception() is not None:
            print("Task error %s (callback)" % future.exception())
        else:
            print("Task is done with result %d (callback)" % future.result())

    def start_async_task(self, thread_event: threading.Event) -> None:

        print("About to create an asyncio task")

        self.task = asyncio.run_coroutine_threadsafe(self.process_task(), asyncio.get_running_loop())
        self.task.add_done_callback(self.task_done)

        print("asyncio task is set up")
        thread_event.set()

    # This method is supposed to be the last call to the application,
    # which shuts down all services and cancels all outstanding work.
    async def shutdown(self) -> None:

        # Calls the done callback immediately and returns before the
        # future cancels the underlying asyncio task, rendering the
        # future unusable via standard methods.
        self.task.cancel()

        # This event compensates for lack of ability to wait for the
        # underlying asyncio task. Without this wait, asyncio task
        # runs after the code that manages all this is gone.
        #
        # Perhaps Future.cancel() should provide this functionality?
        #
        #print("Waiting for a task to complete")
        #await self.task_event.wait()

        # returns True, while underlying asyncio task is still running
        print("Cancelled?: %s" % self.task.cancelled())
        print("Done?: %s" % self.task.done())

        # supposed to wait for result, but because it's cancelled, will throw
        try:
            print("Result?: %d" % self.task.result())
        except concurrent.futures.CancelledError:
            print("Cannot access task.result()")

        # or wait for exception, but because it's cancelled, will throw as well
        try:
            print("Exception?: %s" % str(self.task.exception()))
        except concurrent.futures.CancelledError:
            print("Cannot access task.exception()")

async def main() -> None:
    myapp = MyApp()

    thread_event = threading.Event()
    thread_event.clear()

    # emulates some worker thread (e.g. APScheduler)
    runner = threading.Thread(target=myapp.start_async_task, args=[thread_event])
    runner.run()

    thread_event.wait()

    await asyncio.sleep(1)

    await myapp.shutdown()

    await asyncio.sleep(0)

    print("All done. No app code should run after this.")

asyncio.run(main())