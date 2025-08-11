from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from states.form import Form
from filters.filters import AdminFilter, AddedAdminFilter, MultipleFilter
from functions.format import escape_markdown
from keyboards.form import kb_confirm, kb_start
from functions.config import settings
from functions.redis import list_admins, save_msg

router = Router()

@router.message(StateFilter("*"), F.text == "НАЗАД⬅️")
async def BackHandler(message: Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == Form.name:
        await message.answer("Действие невозможно\.")
        return
    elif current_state == Form.done:
        await message.answer("Вы уже отправили анкету\.")
        return
    
    previous = None
    for step in Form.__all_states__:
        if step.state == current_state:
            match step.state:
                case Form.direction:
                    await StartHandler(message, state)
                    return
                case Form.about:
                    await NameHandler(message, state)
                    return
                case Form.confirm:
                    await DirectionHandler(message, state)
                    return
        previous = step

@router.callback_query(StateFilter(None), F.data == "start")
async def StartHandler(event: CallbackQuery | Message, state: FSMContext):
    if isinstance(event, Message):
        await event.answer("Как вас зовут и сколько вам лет?")
    else:
        await event.message.answer("Как вас зовут и сколько вам лет?", reply_markup=kb_start)
    await state.set_state(Form.name)

@router.message(Form.name, F.text)
async def NameHandler(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Какое направление вам интересно?")
    await state.set_state(Form.direction)

@router.message(Form.direction, F.text)
async def DirectionHandler(message: Message, state: FSMContext):
    await state.update_data(direction=message.text)
    await message.answer("Расскажи о своём опыте и в чём хотели бы себя попробовать\!")
    await state.set_state(Form.about)

@router.message(Form.about, F.text)
async def AboutHandler(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    msg = (
        "__***Ваша анкета:***__\n"
        "👤 ***Имя:*** {name}\n"
        "⚙️ ***Направление:*** {direction}\n"
        "💼 ***Опыт:*** {about}\n"
    ).format(
        name=escape_markdown(await state.get_value("name")),
        direction=escape_markdown(await state.get_value("direction")),
        about=escape_markdown(await state.get_value("about"))
    )
    await message.answer(msg, reply_markup=kb_confirm)
    await state.set_state(Form.confirm)

@router.callback_query(Form.confirm, F.data == "send")
async def SendHandler(callback: CallbackQuery, state: FSMContext):
    msg = (
        "👤 ***Имя:*** {name}\n"
        "⚙️ ***Направление:*** {direction}\n"
        "💼 ***Опыт:*** {about}\n"
    ).format(
        name=escape_markdown(await state.get_value("name")),
        direction=escape_markdown(await state.get_value("direction")),
        about=escape_markdown(await state.get_value("about"))
    )
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Принять ✅",
                    callback_data=f"a{callback.from_user.id}"
                ),
                InlineKeyboardButton(
                    text="Отказать ❌",
                    callback_data=f"r{callback.from_user.id}"
                )
            ]
        ]
    )
    for admin in set(settings.ADMINS) | set(await list_admins()):
        sent = await callback.bot.send_message(chat_id=admin, text=msg, reply_markup=kb)
        await save_msg(user_id=callback.from_user.id, chat_id=sent.chat.id, message_id=sent.message_id)

    await callback.message.edit_text(text="Ваша анкета отправлена\!", reply_markup=None)
    await state.set_data({})
    await state.set_state(Form.done)

@router.callback_query(Form.confirm, F.data == "clear")
async def ClearHandler(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    await StartHandler(callback, state)

@router.callback_query(~MultipleFilter(), Form.done)
async def DoneHandler(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Вы уже отправили анкету.")