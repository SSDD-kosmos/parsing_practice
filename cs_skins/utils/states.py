from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    min_price = State()
    max_price = State()
    min_discount = State()
