from aiogram import F, Router, Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart
from bot.keyboards.reply.choice_buttons import menu, edit_theme_keyboard, go_to_main_menu
from bot.states.sostoy import qfeed_state
from main import db
from aiokafka import AIOKafkaConsumer

async def get_messages_from_kafka():
    consumer = AIOKafkaConsumer(
        'qfeed',
        bootstrap_servers='localhost:9092'
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value, msg.timestamp)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

form_router = Router()


@form_router.message(CommandStart(), F.chat.type.in_({"group", "supergroup"}))
async def start(message: Message, state: FSMContext):
    if message.chat.is_forum:
        await message.answer("Привет, {0}! Добро пожаловать в Qfeed, бота для помощи в организации твоих каналов.\
        Давай начнем! Выбери, что ты хочешь сделать".format(message.from_user.first_name), reply_markup=menu)
        username = message.from_user.username if message.from_user.username is not None else message.from_user.first_name
        db.add_user(message.from_user.id, message.chat.id, username)
        await state.set_state(qfeed_state.main_menu)
    else:
        await message.answer('Для начала работы создай форум, добавь меня в него и сделай администратором. Инструкция, как это сделать: ...')


@form_router.message(F.text == 'Вернуться в меню')
async def to_main_menu(message: Message, state: FSMContext):
    await message.answer('Вы в главном меню', reply_markup=menu)
    await state.set_state(qfeed_state.main_menu)


@form_router.message(qfeed_state.main_menu, F.text == "Добавить тему")
async def add_topic_ask(message: Message, state: FSMContext):
    await message.answer("Напиши название темы", reply_markup=go_to_main_menu)
    await state.set_state(qfeed_state.add_topic)


@form_router.message(qfeed_state.add_topic)
async def add_topic(message: Message, bot: Bot, state: FSMContext):
    forum_topic = await bot.create_forum_topic(message.chat.id, message.text)
    await message.answer(f"Ваша тема {message.text} создана", reply_markup=menu)
    db.add_topic(forum_topic.message_thread_id, forum_topic.name, message.chat.id)
    await state.set_state(qfeed_state.main_menu)

@form_router.message(qfeed_state.main_menu, F.text == "Удалить тему")
async def delete_topic_ask(message: Message, state: FSMContext):
    #TODO у вас нет тем, темы выбираются кнопкой
    user_topics = db.get_topics(message.chat.id)
    if len(user_topics) == 0:
        await message.answer('У Вас нет тем, для начала добавьте их', reply_markup=menu)
        await state.set_state(qfeed_state.main_menu)
    else:
        buttons = []
        for topic in user_topics:
            buttons.append([InlineKeyboardButton(text=topic[0], callback_data=topic[1])])
        topics_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer("Какую тему Вы хотите удалить?", reply_markup=topics_keyboard)
        await state.set_state(qfeed_state.delete_topic)


@form_router.callback_query(qfeed_state.delete_topic)
async def delete_topic(call: CallbackQuery, state: FSMContext, bot: Bot):
    topic_id = call.data
    db_result = db.delete_topic(topic_id=topic_id, chat_id=call.message.chat.id)
    bot_result = await bot.delete_forum_topic(call.message.chat.id, topic_id)
    answer_text = 'Тема успешно удалена' if (db_result and bot_result) else 'Удалить не получилось'
    await call.message.answer(answer_text, reply_markup=menu)
    await call.answer()
    await state.set_state(qfeed_state.main_menu)


@form_router.message(qfeed_state.main_menu, F.text == "Редактировать тему")
async def edit_topic_ask(message: Message, state: FSMContext):
    #TODO у вас нет тем, темы выбираются кнопкой
    user_topics = db.get_topics(message.chat.id)
    if len(user_topics) == 0:
        await message.answer('У Вас нет тем, для начала добавьте их', reply_markup=menu)
        await state.set_state(qfeed_state.main_menu)
    else:
        buttons = []
        for topic in user_topics:
            buttons.append([InlineKeyboardButton(text=topic[0], callback_data=topic[1])])
        topics_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer("Какую тему Вы ходите редактировать?", reply_markup=topics_keyboard)
        await state.set_state(qfeed_state.edit_topic)


@form_router.callback_query(qfeed_state.edit_topic)
async def edit_topic(call: CallbackQuery, state: FSMContext):
    await state.set_data({"call": call})
    await call.message.answer("Что вы хотите сделать?", reply_markup=edit_theme_keyboard)
    await call.answer()
    await state.set_state(qfeed_state.edit_topic_choice)
    

@form_router.message(qfeed_state.edit_topic_choice, F.text == "Добавить канал")
async def add_channel_ask(message: Message, state: FSMContext):
    await message.answer("Отправьте ссылку на канал в формате @tg_channel", reply_markup=go_to_main_menu)
    await state.set_state(qfeed_state.add_channel)


@form_router.message(qfeed_state.edit_topic_choice, F.text == "Удалить канал")
async def delete_channel_ask(message: Message, state: FSMContext):
    call = (await state.get_data())['call']
    user_channels = db.get_channels(message.chat.id, call.data)
    if len(user_channels) == 0:
        await message.answer('В выбранной теме нет каналов, для начала добавьте их', reply_markup=menu)
        await state.set_state(qfeed_state.main_menu)
    else:
        buttons = []
        for channel in user_channels:
            buttons.append([InlineKeyboardButton(text=channel[1], callback_data=channel[0])])
        channels_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer("Выберите канал, который хотите удалить", reply_markup=channels_keyboard)
        await state.set_state(qfeed_state.delete_channel)


@form_router.message(qfeed_state.add_channel)
async def add_channel(message: Message, bot: Bot, state: FSMContext):
    call = (await state.get_data())['call']
    channel_username = message.text
    try:
        chat = await bot.get_chat(channel_username)
        result = db.add_channel(chat.id, chat.title, call.data, message.chat.id)
        answer_text = 'Канал успешно добавлен' if result else 'Канал уже добавлен'
        answer_text += '. Для того, чтобы добавить еще один, отправьте ссылку на канал в формате @tg_channel'
        await message.answer(answer_text, reply_markup=go_to_main_menu)
    except Exception as e:
        print(e)
        await message.answer('Канал не найден. Попробуйте еще раз', reply_markup=go_to_main_menu)


@form_router.callback_query(qfeed_state.delete_channel)
async def delete_channel(call: CallbackQuery, bot: Bot, state: FSMContext):
    topic_id = (await state.get_data())['call'].data
    channel_id = call.data
    result = db.delete_channel(topic_id, call.message.chat.id, channel_id)
    answer_text = 'Канал успешно удален' if result else 'Произошла ошибка'
    await call.message.answer(answer_text, reply_markup=menu)
    await state.set_state(qfeed_state.main_menu)


@form_router.message(qfeed_state.main_menu, F.text == "Настройки")
async def settings_ask(message: Message, state: FSMContext):
    #TODO изменение языка, обратная связь
    await message.answer("Что Вы хотите сделать?", reply_markup=go_to_main_menu)
    await state.set_state(qfeed_state.settings)


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


@form_router.message(F.chat.type.not_in({"group", "supergroup"}))
async def process_unknown_write_bots(message: Message) -> None:
    await message.reply("Для начала работы создай форум, добавь меня в него и сделай администратором. Инструкция, как это сделать: ...")


@form_router.message()
async def dont_understand(message: Message, state: FSMContext) -> None:
    if not message.from_user.is_bot and message.text is not None:
        if state.get_state() == qfeed_state.main_menu:
            await message.reply('Не понимаю Вас')
        else:
            await message.reply('Не понимаю Вас, хотите вернуться в меню?', reply_markup=go_to_main_menu)
