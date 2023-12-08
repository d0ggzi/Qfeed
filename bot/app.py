# - *- coding: utf- 8 - *-

import logging
from aiogram import Bot, Dispatcher, enums
from aiogram.fsm.storage.memory import MemoryStorage
from bot.handlers import form_router, admin_router, start_router
import asyncio
from config import settings
import sys

async def main():
    bot = Bot(token=settings.BOT_TOKEN, parse_mode=enums.ParseMode.HTML)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_routers(admin_router, form_router, start_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
