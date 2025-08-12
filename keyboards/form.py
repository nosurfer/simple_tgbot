from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

kb_confirm = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Отправить ✅",
                callback_data="send"
            ),
            InlineKeyboardButton(
                text="Сбросить ↩️",
                callback_data="clear"
            )
        ]
    ]
)

kb_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="НАЗАД⬅️"
            )
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Напишите ответ на вопрос:"
)

spec_choice_kb = InlineKeyboardBuilder(
    markup=[
        [
            InlineKeyboardButton(
                text="Актёр",
                callback_data=f"Актёр"
            ),
            InlineKeyboardButton(
                text="Режиссёр",
                callback_data=f"Режиссёр"
            ),
            InlineKeyboardButton(
                text="Сценарист",
                callback_data=f"Сценарист"
            ),
            InlineKeyboardButton(
                text="Продакшн",
                callback_data=f"Продакшн"
            )
        ]
    ]).adjust(2,).as_markup()
