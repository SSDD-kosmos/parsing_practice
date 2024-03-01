import time
import json

from aiogram import Router
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hlink

from cs_skins.data.main import Collection
from . import settings

router = Router()


@router.message()
async def get_discount(message: Message):
    await message.answer('Please waiting...')
    msg = message.text.lower()
    if len(settings.formatted_text) > 3:
        settings.formatted_text = settings.formatted_text[3:]

    if msg == '🔪 knives':
        col = Collection(weapon_type=2)
        if len(settings.formatted_text) > 0:
            col.collect_data(minPrice=settings.formatted_text[0],
                             maxPrice=settings.formatted_text[1],
                             discount=settings.formatted_text[2])
        else:
            col.collect_data()
        col.save()
    elif msg == '🥊 gloves':
        col = Collection(weapon_type=13)
        if len(settings.formatted_text) > 0:
            col.collect_data(minPrice=settings.formatted_text[0],
                             maxPrice=settings.formatted_text[1],
                             discount=settings.formatted_text[2])
        else:
            col.collect_data()
        col.save()
    elif msg == '🔫 sniper rifles':
        col = Collection(weapon_type=4)
        if len(settings.formatted_text) > 0:
            col.collect_data(minPrice=settings.formatted_text[0],
                             maxPrice=settings.formatted_text[1],
                             discount=settings.formatted_text[2])
        else:
            col.collect_data()
        col.save()

    with open('result.json') as file:
        data = json.load(file)

    for index, item in enumerate(data):
        card = f'{hlink(item.get("full_name"), item.get("item_3d"))}\n' \
               f'{hbold("Discount: ")}{item.get("item_discount")}%\n' \
               f'{hbold("Price: ")}${item.get("item_price")}🔥'

        if index % 20 == 0:
            time.sleep(3)

        await message.answer(card)
    print(len(settings.formatted_text))
