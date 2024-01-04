from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

city = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Saint-Petersburg'),
            KeyboardButton(text='Moscow'),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Choose the city',
    selective=True,
)
