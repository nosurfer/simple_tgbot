from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from keyboards.start import keyboard

router = Router()

@router.message(CommandStart())
async def StartHandler(message: Message):
    await message.answer("Привет\! Бот сделан @ownnickname\.", reply_markup=keyboard)