import asyncio

detection_queue: asyncio.Queue = asyncio.Queue()

async def get_queue() -> asyncio.Queue:
    return detection_queue