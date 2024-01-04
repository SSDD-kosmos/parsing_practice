from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold

from cs_skins.keyboards import reply
from cs_skins.filters.is_admin import IsAdmin

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!\n Choose category...",
                         reply_markup=reply.guns)


@router.message(F.text.lower().in_(['hi', 'hello', 'good morning']))
async def greetings(message: Message):
    await message.reply('Heeellooo')
