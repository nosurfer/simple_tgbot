import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder

from functions.redis import get_redis
from functions.config import settings
from handlers import get_routers

async def setup_storage(retries: int = 10, delay: float = 1.0):
    redis_ = await get_redis()
    for attempt in range(1, retries + 1):
        try:
            await redis_.ping()
            break
        except Exception as e:
            if attempt == retries:
                await redis_.close()
                raise RuntimeError(f"Cannot connect to Redis at {redis_url}: {e}") from e
            await asyncio.sleep(delay)
    return RedisStorage(redis=redis_, key_builder=DefaultKeyBuilder(with_bot_id=True))

async def setup_handlers(dp: Dispatcher) -> None:
    for r in get_routers():
        dp.include_router(r)

async def main():
    global bot
    bot = Bot(token=settings.TOKEN, default=DefaultBotProperties(parse_mode="MarkdownV2"))
    dp = Dispatcher(storage=await setup_storage())

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    await setup_handlers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())