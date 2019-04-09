import asyncio
from aiopg.utils import ClosableQueue


async def test_closable_queue_noclose():
    queue = ClosableQueue()
    await queue.put(1)
    v = await queue.get()
    assert v == 1


async def test_closable_queue_close(loop):
    queue = ClosableQueue()
    v1 = None

    async def read():
        nonlocal v1
        v1 = await queue.get()
        await queue.get()

    reader = loop.create_task(read())
    await queue.put(1)
    await asyncio.sleep(0.1)
    assert v1 == 1

    queue.close(RuntimeError("connection closed"))
    try:
        await reader
    except RuntimeError as ex:
        assert ex.args == ("connection closed",)
