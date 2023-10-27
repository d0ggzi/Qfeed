import logging
from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from config import admin_id
from bot.keyboards.inline.choice_buttons import admin_keyboard
from aiogram.fsm.context import FSMContext
from aiogram.filters import BaseFilter
from bot.filters.admin import IsAdmin

from aiogram.types import Message
from bot.states.sostoy import qfeed_state


start_router = Router()


@start_router.message(IsAdmin(), F.chat.type.not_in({"group", "supergroup"}), Command(commands=["start"]))
async def if_admin_start(message: Message, state: FSMContext):
    await message.answer("Добро пожаловать, админ!", reply_markup=admin_keyboard)
    await state.set_state(qfeed_state.main_menu)


@start_router.message(F.chat.type.not_in({"group", "supergroup"}), Command(commands=["start"]))
async def if_not_admin_start(message: Message, state: FSMContext):
    await message.answer(
            "Для начала работы создай форум, добавь меня в него и сделай администратором. Инструкция, как это сделать: ...")
    await state.set_state(qfeed_state.main_menu)
