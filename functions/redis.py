import redis.asyncio as redis_asyncio
from functions.config import settings

ADMINS_KEY: str = "admins"
redis_: redis_asyncio.Redis | None = None

async def get_redis():
    global redis_
    if redis_ is None:
        redis_ = redis_asyncio.Redis(host=settings.REDIS, port=6379, db=0)
    return redis_

async def is_admin(user_id: int | str) -> bool:
    if isinstance(user_id, int):
        user_id = str(user_id)
    r = await get_redis()
    return await r.sismember(ADMINS_KEY, user_id)

async def add_admin(user_id: int | str) -> bool:
    if isinstance(user_id, int):
        user_id = str(user_id)
    r = await get_redis()
    added = await r.sadd(ADMINS_KEY, user_id)
    return bool(added)

async def remove_admin(user_id: int | str) -> bool:
    if isinstance(user_id, int):
        user_id = str(user_id)
    r = await get_redis()
    removed = await r.srem(ADMINS_KEY, user_id)
    return bool(removed)

async def list_admins() -> list[int]:
    r = await get_redis()
    return [int(uid.decode()) for uid in await r.smembers(ADMINS_KEY)]

async def save_msg(user_id: int | str, chat_id: int, message_id: int) -> bool:
    if isinstance(user_id, int):
        user_id = str(user_id)
    r = await get_redis()
    added = await r.rpush(user_id, f"{chat_id}:{message_id}")
    return bool(added)

async def get_all_msgs(user_id: int | str) -> list[dict[str, int]]:
    if isinstance(user_id, int):
        user_id = str(user_id)
    r = await get_redis()
    raw_list = await r.lrange(user_id, 0, -1)  # Get all elements from list
    result = []
    for item in raw_list:
        decoded = item.decode()
        chat_id_str, message_id_str = decoded.split(":")
        result.append({
            "chat_id": int(chat_id_str),
            "message_id": int(message_id_str)
        })
    await r.delete(user_id)
    return result



