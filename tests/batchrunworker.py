import asyncio
from string import ascii_uppercase
from typing import List

TASK_NAMES = ascii_uppercase  # 26 fake tasks in total


class BatchWorker:
    """Run a list of tasks in batch."""

    BATCH_SIZE = 10

    def __init__(self, tasks: List[asyncio.Task],BATCH_SIZE=10):
        self._tasks = list(tasks)
        self._BATCH_SIZE=BATCH_SIZE
    @property
    def batch_of_tasks(self):
        """Yield all tasks by chunks of `BATCH_SIZE`"""
        start = 0
        while 'there are items remaining in the list':
            end = start + self._BATCH_SIZE
            chunk = self._tasks[start:end]
            if not chunk:
                break
            yield chunk
            start = end

    async def run(self):
        print(f'Running {self._BATCH_SIZE} tasks at a time')
        for batch in self.batch_of_tasks:
            print(f'\nWaiting for {len(batch)} tasks to complete...')
            await asyncio.gather(*batch)
            print('\nSleeping...\n---')
            await asyncio.sleep(1)


    async def cancel_waiting_task(work_task, waiting_task):
        await asyncio.sleep(2)
        waiting_task.cancel()
        try:
            await waiting_task
            print("Waiting done")
        except asyncio.CancelledError:
            print("Waiting task cancelled")

        try:
            res = await work_task
            print(f"Work result: {res}")
        except asyncio.CancelledError:
            print("Work task cancelled")
async def task(name: str):
    print(f"Task '{name}' is running...")
    if name=='A':
        print('task failed')
    else:
        print('task ok')
    await asyncio.sleep(3)  # Pretend to do something


async def main():
    tasks = [task(name) for name in TASK_NAMES]
    worker = BatchWorker(tasks)
    await worker.run()


if __name__ == '__main__':
    asyncio.run(main())