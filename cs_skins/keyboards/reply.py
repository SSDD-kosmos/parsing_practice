from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)

guns = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🔪 Knives'),
            KeyboardButton(text='🥊 Gloves'),
            KeyboardButton(text='🔫 Sniper rifles'),
        ],
        [
            KeyboardButton(text='Settings')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Choose category',
    selective=True,
)

rmk = ReplyKeyboardRemove()
