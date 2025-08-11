from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.filters import StateFilter

from keyboards.start import keyboard

router = Router()

@router.message(StateFilter(None), CommandStart())
async def StartHandler(message: Message):
    await message.answer("Привет\! У тебя будет одна попытка\. Бот сделан @ownnickname\.", reply_markup=keyboard)