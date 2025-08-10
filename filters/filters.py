from typing import Union
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from functions.config import settings  # your ADMINS list

class AdminFilter(BaseFilter):
    async def __call__(self, event: Union[Message, CallbackQuery]) -> bool:
        user = getattr(event, "from_user", None)
        if not user:
            return False
        return int(user.id) in set(map(int, settings.ADMINS))
