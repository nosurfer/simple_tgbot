from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

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
    ]
)
