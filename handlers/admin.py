from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states.admin import OwnMessage
from states.form import Form
from functions.config import settings
from filters.filters import AdminFilter, AddedAdminFilter, MultipleFilter
from keyboards.admin import *
from functions.redis import *

router = Router()

@router.callback_query(MultipleFilter(), F.data.regexp(r"^a\d+$"))
async def AcceptHandler(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=await choice_kb(callback))

@router.callback_query(MultipleFilter(), F.data.regexp(r"^r\d+$"))
async def DenyHandler(callback: CallbackQuery):
    user_id = int(callback.data[1:])
    await update_messages(callback, user_id, denied)
    await callback.bot.send_message(chat_id=user_id, text=await send_denied(), parse_mode=None)

@router.callback_query(MultipleFilter(), F.data.regexp(r"^T\d_\d+$"))
async def TypeHandler(callback: CallbackQuery, state: FSMContext):
    T = callback.data[1]
    user_id = int(callback.data[3:])
    match T:
        case "1":
            await callback.bot.send_message(chat_id=user_id, text=await send_accept({settings.ACTORS}), parse_mode=None)
        case "2":
            await callback.bot.send_message(chat_id=user_id, text=await send_accept({settings.DIRECTORS}), parse_mode=None)
        case "3":
            await callback.bot.send_message(chat_id=user_id, text=await send_accept({settings.SCENARISTS}), parse_mode=None)
        case "4":
            await callback.bot.send_message(chat_id=user_id, text=await send_accept({settings.PRODUCTION}), parse_mode=None)
        case "5":
            await callback.message.edit_reply_markup(reply_markup=None)
            await callback.message.answer("Введите своё сообщение:")
            await state.clear()
            await state.set_state(OwnMessage.message)
            await state.update_data(user_id=user_id)
            return

    await update_messages(callback, user_id, accepted)

@router.message(OwnMessage.message)
async def ForwardHandler(message: Message, state: FSMContext):
    user_id = await state.get_value("user_id")
    try:
        await message.bot.copy_message(
            chat_id=user_id,
            from_chat_id=message.chat.id,
            message_id=message.message_id,
        )
    except:
        await message.answer("Сообщение не удалось отправить :(", parse_mode=None)
    await update_messages(message, user_id, accepted)
    await state.clear()
    await state.set_state(Form.done)

@router.callback_query(MultipleFilter(), F.data == "submited")
async def BufHandler(callback: CallbackQuery):
    await callback.answer("Сообщение уже было отправлено.")

@router.message(AdminFilter(), Command("admin"))
async def add_handler(message: Message):
    await message.answer("Выберите пользователя, чтобы изменить статус администратора\.", reply_markup=admin_kb)

@router.message(AdminFilter(), F.user_shared.request_id == 1)
async def admin_handler_user_shared(message: Message):
    user_id = message.user_shared.user_id
    await toggle_admin_status(message, user_id)

@router.message(AdminFilter(), F.contact)
async def admin_handler_contact(message: Message):
    if not message.contact.user_id:
        await message.answer("Этот контакт не привязан к Telegram-аккаунту.")
        return
    user_id = message.contact.user_id
    await toggle_admin_status(message, user_id)

async def toggle_admin_status(message: Message, user_id: int):
    if await is_admin(user_id):
        await remove_admin(user_id)
        await message.answer(
            "Пользователь больше не админ 😭",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await add_admin(user_id)
        await message.answer(
            "Пользователь стал админом 🎉",
            reply_markup=ReplyKeyboardRemove()
        )

async def update_messages(event: Message | CallbackQuery, user_id: int, kb: InlineKeyboardMarkup) -> None:
    for msg in await get_all_msgs(user_id=user_id):
        chat_id = msg['chat_id']
        message_id = msg['message_id']
        try:
            await event.bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=kb)
        except:
            continue