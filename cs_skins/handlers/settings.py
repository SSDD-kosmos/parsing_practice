from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from cs_skins.utils.states import Form
from cs_skins.keyboards.builders import settings_builder
from cs_skins.keyboards.reply import guns


router = Router()
formatted_text = []


@router.message(F.text.lower() == 'settings')
async def fill_settings(message: Message, state: FSMContext):
    await state.set_state(Form.min_price)
    await message.answer(
        'Enter the minimum price...',
        reply_markup=settings_builder(['100', '500', '1000', '2000', '3000'])
    )


@router.message(Form.min_price)
async def form_min_price(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(min_price=message.text)
        await state.set_state(Form.max_price)
        await message.answer('Great, now enter the maximum price...',
                             reply_markup=settings_builder(['2000', '3000', '4000', '5000']))
    else:
        await message.answer('Enter the number again...')


@router.message(Form.max_price)
async def form_max_price(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(max_price=message.text)
        await state.set_state(Form.min_discount)
        await message.answer(
            'Great, now enter the minimum discount... \n (number)',
            reply_markup=settings_builder(['5', '10', '15', '20', '25', '30'])
        )
    else:
        await message.answer('Enter the number again...')


@router.message(Form.min_discount)
async def form_min_discount(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(min_discount=message.text)
        data = await state.get_data()
        await state.clear()

        [formatted_text.append(f'{value}') for key, value in data.items()]

        await message.answer('Your settings is save. \n Choose category...', reply_markup=guns)
    else:
        await message.answer('Enter the number again...')
