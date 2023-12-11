import asyncio
from typing import Optional, Tuple, Set


async def wait_any(
        tasks: Set[asyncio.Future], *, timeout: Optional[int] = None,
) -> Tuple[Set[asyncio.Future], Set[asyncio.Future]]:
    tasks_to_cancel: Set[asyncio.Future] = set()
    try:
        done, tasks_to_cancel = await asyncio.wait(
            tasks, timeout=timeout, return_when=asyncio.FIRST_COMPLETED
        )
        return done, tasks_to_cancel
    except asyncio.CancelledError:
        tasks_to_cancel = tasks
        raise
    finally:
        for task in tasks_to_cancel:
            task.cancel()


async def task():
    await asyncio.sleep(5)


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


async def check_tasks(waiting_task, working_task, waiting_conn_lost_task):
    try:
        await waiting_task
        print("waiting is done")
    except asyncio.CancelledError:
        print("waiting is cancelled")

    try:
        await waiting_conn_lost_task
        print("connection is lost")
    except asyncio.CancelledError:
        print("waiting connection lost is cancelled")

    try:
        await working_task
        print("work is done")
    except asyncio.CancelledError:
        print("work is cancelled")


async def work_done_case():
    working_task = asyncio.create_task(task())
    connection_lost_event = asyncio.Event()
    waiting_conn_lost_task = asyncio.create_task(connection_lost_event.wait())
    waiting_task = asyncio.create_task(wait_any({working_task, waiting_conn_lost_task}))
    await check_tasks(waiting_task, working_task, waiting_conn_lost_task)


async def conn_lost_case():
    working_task = asyncio.create_task(task())
    connection_lost_event = asyncio.Event()
    waiting_conn_lost_task = asyncio.create_task(connection_lost_event.wait())
    waiting_task = asyncio.create_task(wait_any({working_task, waiting_conn_lost_task}))
    await asyncio.sleep(2)
    connection_lost_event.set()  # <---
    await check_tasks(waiting_task, working_task, waiting_conn_lost_task)


async def cancel_waiting_case():
    working_task = asyncio.create_task(task())
    connection_lost_event = asyncio.Event()
    waiting_conn_lost_task = asyncio.create_task(connection_lost_event.wait())
    waiting_task = asyncio.create_task(wait_any({working_task, waiting_conn_lost_task}))
    await asyncio.sleep(2)
    waiting_task.cancel()  # <---
    await check_tasks(waiting_task, working_task, waiting_conn_lost_task)


async def main():
    print("Work done")
    print("-------------------")
    await work_done_case()
    print("\nConnection lost")
    print("-------------------")
    await conn_lost_case()
    print("\nCancel waiting")
    print("-------------------")
    await cancel_waiting_case()


asyncio.run(main())