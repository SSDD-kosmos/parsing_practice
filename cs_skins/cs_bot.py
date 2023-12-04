import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from main import Collection
import os
import asyncio
from cs_token import token
import time


bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


class Settings:

    def __init__(self, minPrice=4000, maxPrice=10000, discount=0.25):
        self.minPrice = minPrice
        self.maxPrice = maxPrice
        self.discount = discount

    @dp.message_handler(commands='settings')
    async def settings(self, message: types.Message):
        settings_buttons = ['Min price', 'Max price', 'Min discount']
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*settings_buttons)

        await message.answer('Choose setting', reply_markup=keyboard)

    # @dp.message_handler(Text(equals='Min price'))
    # async def get_min_price(self: types.Message):
    #     await self.answer('Please waiting...')
    #
    # @dp.message_handler(Text(equals='Max price'))
    # async def get_max_price(self: types.Message):
    #     await self.answer('Please waiting...')
    #
    # @dp.message_handler(Text(equals='Min discount'))
    # async def get_discount(self: types.Message):
    #     await self.answer('Please waiting...')


class Start(Settings):

    def __init__(self, minPrice=4000, maxPrice=10000, discount=0.25):
        super().__init__(minPrice, maxPrice, discount)

    @dp.message_handler(commands='start')
    async def start(self, message: types.Message):
        start_buttons = ['🔪 Knives', '🥊 Gloves', '🔫 Sniper rifles']
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*start_buttons)

        # await bot.send_message(message.from_user.id, message.from_user.first_name)
        await message.answer('Choose category', reply_markup=keyboard)

    @dp.message_handler(Text(equals='🔪 Knives'))
    async def get_discount_knives(self, message: types.Message):
        await message.answer('Please waiting...')

        col = Collection(weapon_type=2)
        col.collect_data(minPrice=self.minPrice, maxPrice=self.maxPrice, discount=self.discount)
        col.save()

        with open('result.json') as file:
            data = json.load(file)

        for index, item in enumerate(data):
            card = f'{hlink(item.get("full_name"), item.get("item_3d"))}\n' \
                   f'{hbold("Скидка: ")}{item.get("item_discount")}%\n' \
                   f'{hbold("Цена: ")}${item.get("item_price")}🔥'

            if index % 20 == 0:
                time.sleep(3)

            await message.answer(card)

    @dp.message_handler(Text(equals='🥊 Gloves'))
    async def get_discount_gloves(self, message: types.Message):
        await message.answer('Please waiting...')

        col = Collection(weapon_type=13)
        col.collect_data(minPrice=self.minPrice, maxPrice=self.maxPrice, discount=self.discount)
        col.save()

        with open('result.json') as file:
            data = json.load(file)

        for index, item in enumerate(data):
            card = f'{hlink(item.get("full_name"), item.get("item_3d"))}\n' \
                   f'{hbold("Скидка: ")}{item.get("item_discount")}%\n' \
                   f'{hbold("Цена: ")}${item.get("item_price")}🔥'

            if index % 20 == 0:
                time.sleep(3)

            await message.answer(card)

    @dp.message_handler(Text(equals='🔫 Sniper rifles'))
    async def get_discount_sniper_rifles(self, message: types.Message):
        await message.answer('Please waiting...')

        col = Collection(weapon_type=4)
        col.collect_data(minPrice=self.minPrice, maxPrice=self.maxPrice, discount=self.discount)
        col.save()

        with open('result.json') as file:
            data = json.load(file)

        for index, item in enumerate(data):
            card = f'{hlink(item.get("full_name"), item.get("item_3d"))}\n' \
                   f'{hbold("Скидка: ")}{item.get("item_discount")}%\n' \
                   f'{hbold("Цена: ")}${item.get("item_price")}🔥'

            if index % 20 == 0:
                time.sleep(3)

            await message.answer(card)


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
