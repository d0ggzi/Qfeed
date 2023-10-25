import logging

from aiogram import Router, F, Bot
from aiogram.filters import BaseFilter
from config import admin_id
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart
from main import db
from bot.states.mailing import bot_mailing

admin_router = Router()


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == int(admin_id)


@admin_router.message(IsAdmin(), F.chat.type.not_in({"group", "supergroup"}), F.text == 'Отправить рекламу')
async def mailing(message: Message, state: FSMContext):
    await message.answer(text='Напишите текст рекламы в следующем сообщении')
    await state.set_state(bot_mailing.text)


@admin_router.message(IsAdmin(), F.chat.type.not_in({"group", "supergroup"}), state=bot_mailing.text)
async def start_mailing(message: Message, state: FSMContext):
    chats = db.get_all_users()
    answer = message.text
    for chat in chats:
        await bot.send_message(chat, answer)

    await state.set_state(state=bot_mailing.main_menu)

