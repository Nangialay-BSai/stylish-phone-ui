import asyncio
from typing import AsyncIterator
from redis import asyncio as aioredis
from ..core.config import settings


redis_async = aioredis.from_url(settings.REDIS_URL, decode_responses=True)


async def publish(channel: str, message: str) -> None:
    await redis_async.publish(channel, message)


async def subscribe(channel: str) -> AsyncIterator[str]:
    pubsub = redis_async.pubsub()
    await pubsub.subscribe(channel)
    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message and message.get("type") == "message":
                yield str(message.get("data"))
            await asyncio.sleep(0)
    finally:
        await pubsub.unsubscribe(channel)
        await pubsub.close()
