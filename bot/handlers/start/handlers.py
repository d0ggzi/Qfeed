import logging
from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from config import admin_id
from bot.keyboards.inline.choice_buttons import admin_keyboard
from aiogram.filters import BaseFilter
from aiogram.types import Message


start_router = Router()


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == int(admin_id)


@start_router.message(IsAdmin(), F.chat.type.not_in({"group", "supergroup"}), Command(commands=["start"]))
async def if_admin_start(message: Message):
    await message.answer("Добро пожаловать, админ!", reply_markup=admin_keyboard)


@start_router.message(F.chat.type.not_in({"group", "supergroup"}), Command(commands=["start"]))
async def if_not_admin_start(message: Message):
    await message.answer(
            "Для начала работы создай форум, добавь меня в него и сделай администратором. Инструкция, как это сделать: ...")

