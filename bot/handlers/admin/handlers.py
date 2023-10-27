import logging

from aiogram import Router, F, Bot
from aiogram.filters import BaseFilter
import config
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart
from main import db
from bot.states.mailing import bot_mailing
from bot.states.sostoy import qfeed_state
from bot.filters.admin import IsAdmin

admin_router = Router()


@admin_router.message(qfeed_state.main_menu, IsAdmin(), F.chat.type.not_in({"group", "supergroup"}), F.text == 'Отправить рекламу')
async def mailing(message: Message, state: FSMContext):
    await message.answer(text='Напишите текст рекламы в следующем сообщении')
    await state.set_state(bot_mailing.text)

#
# @admin_router.message(IsAdmin(), F.chat.type.not_in({"group", "supergroup"}), bot_mailing.text)
# async def start_mailing(message: Message, state: FSMContext, bot: Bot):
#     chats = db.get_all_users()
#     answer = message.text
#     for chat in chats:
#         await bot.send_message(chat, answer)
#     await state.set_state(qfeed_state.main_menu)
#


@admin_router.message(IsAdmin(), F.chat.type.not_in({"group", "supergroup"}), bot_mailing.text)
async def start_mailing(message: Message, state: FSMContext, bot: Bot):
    chats = db.get_all_users()
    for chat in chats:
        await message.send_copy(chat)
    await state.set_state(qfeed_state.main_menu)