import logging

from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup
from aiogram.filters import Command, CommandStart
from bot.keyboards.inline.choice_buttons import menu
from bot.states.sostoy import qfeed_state
from main import db
from config import admin_id
from aiogram.filters import BaseFilter

form_router = Router()


@form_router.message(CommandStart(), F.chat.type.in_({"group", "supergroup"}))
async def start(message: Message, state: FSMContext):
    await message.answer("Привет, {0}! Добро пожаловать в Qfeed, бота для помощи в организации твоих каналов.\
        Давай начнем! Выбери, что ты хочешь сделать".format(message.from_user.first_name), reply_markup=menu)
    username = message.from_user.username if message.from_user.username is not None else message.from_user.first_name
    db.add_user(message.from_user.id, message.chat.id, username)
    await state.set_state(qfeed_state.main_menu)


@form_router.message(qfeed_state.main_menu, F.text == "Редактировать тему")
async def edit_theme_ask(message: Message, state: FSMContext):
    #TODO у вас нет тем, темы выбираются кнопкой
    await message.answer("Какую тему Вы ходите редактировать?")
    await state.set_state(qfeed_state.edit_theme)


@form_router.message(qfeed_state.main_menu, F.text == "Добавить тему")
async def add_theme_ask(message: Message, state: FSMContext):
    await message.answer("Напиши название темы")
    await state.set_state(qfeed_state.add_theme)


@form_router.message(qfeed_state.add_theme)
async def add_theme(message: Message, bot: Bot, state: FSMContext):
    forum_topic = await bot.create_forum_topic(message.chat.id, message.text)
    await message.answer(f"Ваша тема {message.text} создана")
    db.add_topic(forum_topic.message_thread_id, forum_topic.name, message.chat.id)
    await state.set_state(qfeed_state.main_menu)


@form_router.message(qfeed_state.main_menu, F.text == "Удалить тему")
async def delete_theme_ask(message: Message, state: FSMContext):
    #TODO у вас нет тем, темы выбираются кнопкой
    topics = db.get_topics(message.chat.id)
    for topic in topics:
        # INLINE KEYBOARD
        pass
    await message.answer("Какую тему Вы хотите удалить?")
    await state.set_state(qfeed_state.delete_theme)


# @form_router.message(qfeed_state.main_menu, F.text == "Настройки")
# async def settings_ask(message: Message, state: FSMContext):
#     #TODO изменение языка, обратная связь
#     await message.answer("Что Вы хотите сделать?")
#     await state.set_state(qfeed_state.settings)


# @form_router.message(sostoy.reply_message)
# async def category(message: Message, state: FSMContext):
#     print(message.text)
#     await message.answer("Теперь выбери лейбл: 0 - обычный пост, 1 - реклама", reply_markup=menu)
#     await state.set_state(sostoy.choose_label)

# @form_router.message(sostoy.choose_label, F.text.in_({"0", "1"}))
# async def category(message: Message, state: FSMContext):
#     print(message.text)
#     await message.answer("Спасибо!")
#     await state.set_state(sostoy.reply_message)


# @form_router.message(F.chat.type.not_in({"group", "supergroup"}))
# async def process_unknown_write_bots(message: Message) -> None:
#     await message.reply(
#             "Для начала работы создай форум, добавь меня в него и сделай администратором. Инструкция, как это")

