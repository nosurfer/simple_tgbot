from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from states.form import Form

from functions.format import escape_markdown

router = Router()

@router.callback_query(StateFilter(None), F.data == "start")
async def NameHandler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Как вас зовут и сколько вам лет?")
    await state.set_state(Form.name)

@router.message(Form.name, F.text)
async def DirectionHandler(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Какое направление тебе интересно?")
    await state.set_state(Form.direction)

@router.message(Form.direction, F.text)
async def AboutHandler(message: Message, state: FSMContext):
    await state.update_data(direction=message.text)
    await message.answer("Расскажи о своём опыте и в чём хотел бы себя попробовать\!")
    await state.set_state(Form.about)

@router.message(Form.about, F.text)
async def ConfirmHandler(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    msg = (
        "__***Ваша анкета***__\n"
        "***Имя:*** {name}\n"
        "***Направление:*** {direction}\n"
        "***Опыт:*** {about}\n"
    ).format(
        name=escape_markdown(await state.get_value("name")),
        direction=escape_markdown(await state.get_value("direction")),
        about=escape_markdown(await state.get_value("about"))
    )
    await message.answer(msg)
    await state.set_state(Form.about)
