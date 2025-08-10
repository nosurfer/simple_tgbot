from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import Command
from main import bot

from filters.filters import AdminFilter
from keyboards.admin import denied, accepted, choice_kb

router = Router()

@router.callback_query(AdminFilter(), F.data.regexp(r"^a\d+$"))
async def AcceptHandler(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=await choice_kb(callback))

@router.callback_query(AdminFilter(), F.data.regexp(r"^r\d+$"))
async def DenyHandler(callback: CallbackQuery):
    user_id = int(callback.data[1:])
    await bot.send_message(chat_id=user_id, text="Увы, на данный момент мы вынуждены вам отказать\.")
    await callback.message.edit_reply_markup(reply_markup=denied)

@router.callback_query(AdminFilter(), F.data.regexp(r"^T\d_\d+$"))
async def TypeHandler(callback: CallbackQuery):
    T = callback.data[1]
    user_id = int(callback.data[3:])
    match T:
        case "1":
            await bot.send_message(chat_id=user_id, text="https://t.me/+PhWy1t-gkyJiYjEyj", parse_mode=None)
        case "2":
            await bot.send_message(chat_id=user_id, text="https://t.me/+LXIh1uuIxu40ZmMy", parse_mode=None)
        case "3":
            await bot.send_message(chat_id=user_id, text="https://t.me/+Qx8nQdzPik42M2Ey", parse_mode=None)
        case "4":
            await bot.send_message(chat_id=user_id, text="https://t.me/+ps2QuNz1_wM3OGNi", parse_mode=None)

    await callback.message.edit_reply_markup(reply_markup=accepted)

@router.callback_query(AdminFilter(), F.data == "submited")
async def BufHandler(callback: CallbackQuery):
    await callback.answer("Сообщение уже было отправлено.")

@router.callback_query(AdminFilter(), Command("/admin"))
async def AddHandler():
    pass