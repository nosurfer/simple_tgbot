import asyncio
import logging
import redis.asyncio as redis_asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder

from functions.config import settings
from handlers import get_routers

def setup_storage():
    redis_client = redis_asyncio.Redis(host="localhost", port=6379, db=0)
    return RedisStorage(redis=redis_client, key_builder=DefaultKeyBuilder(with_bot_id=True))

async def setup_handlers(dp: Dispatcher) -> None:
    for r in get_routers():
        dp.include_router(r)

async def main(bot: Bot, dp: Dispatcher):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    await setup_handlers(dp)
    await dp.start_polling(bot)

bot = Bot(token=settings.TOKEN, default=DefaultBotProperties(parse_mode="MarkdownV2"))
dp = Dispatcher(
    storage=setup_storage()
)

if __name__ == "__main__":
    asyncio.run(main(bot, dp))