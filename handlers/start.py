from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from functions.redis import mark_message_sent, can_send_message
from keyboards.start import *

router = Router()

@router.message(CommandStart())
async def StartHandler(message: Message, state: FSMContext):
    if await can_send_message(message.from_user.id):
        await state.clear()
        await message.answer(text=start_text, reply_markup=keyboard, parse_mode=None)
    else:
        await message.answer(text="Извините, анкету можно отправить только раз в месяц!", parse_mode=None)
