from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery

accepted = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Принято ✅",
                callback_data="submited"
            )
        ]
    ]
)

denied = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Отказано ❌",
                callback_data="submited"
            )
        ]
    ]
)

async def choice_kb(callback: CallbackQuery):
    return InlineKeyboardBuilder(
        markup=[
            [
                InlineKeyboardButton(
                    text="Актёры",
                    callback_data=f"T1_{callback.data[1:]}"
                ),
                InlineKeyboardButton(
                    text="Режиссёры",
                    callback_data=f"T2_{callback.data[1:]}"
                ),
                InlineKeyboardButton(
                    text="Сценаристы",
                    callback_data=f"T3_{callback.data[1:]}"
                ),
                InlineKeyboardButton(
                    text="Продакшн",
                    callback_data=f"T4_{callback.data[1:]}"
                )
            ]
        ]
    ).adjust(2,).as_markup()

admin_kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="👤 Выбрать пользователя",
                    request_users={
                        "request_id": 1,
                        "user_is_bot": False,
                        "max_quantity": 1
                    }
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )