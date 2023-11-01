# - *- coding: utf- 8 - *-

import logging
from aiogram import Bot, Dispatcher, enums
from aiogram.fsm.storage.memory import MemoryStorage
from bot.handlers import form_router, admin_router, start_router, get_messages_from_kafka
import asyncio
import config
import sys



async def counter_loop(x, n):
    for i in range(1, n + 1):
        print(f"Counter {x}: {i}")
        await asyncio.sleep(0.5)
    return f"Finished {x} in {n}"

async def main():
    bot = Bot(token=config.BOT_TOKEN, parse_mode=enums.ParseMode.HTML)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_routers(form_router, start_router, admin_router)
    # dp.startup.register(on_startup_launch)
    # asyncio.create_task(get_message_from_kafka())
    # print('something')
    # await dp.start_polling(bot)
    await asyncio.gather(dp.start_polling(bot), get_messages_from_kafka())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
