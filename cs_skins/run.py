import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from cs_skins.config_reader import config
from cs_skins.handlers import bot_messanges, user_commands, settings


async def main():
    bot = Bot(config.bot_token.get_secret_value(), parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.include_routers(
        user_commands.router,
        settings.router,
        bot_messanges.router,
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
