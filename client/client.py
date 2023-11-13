from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime
from parser import db
import config


app = Client('bot_python', config.API_ID, config.API_HASH)


@app.on_message(filters.chat(db.get_channels()))
async def get_post(client, message: Message):
    await message.forward(config.bot_id)

    # if not db.message_id_exists(username, message_id):
    #     db.add_message_id(username, message_id)
    #     # получение последнего ROWID
    #     for a in db.get_last_rowid():
    #         last_id = a[0]

    #     # перессылка поста на модерку
    #     message.forward(db.get_moder(), as_copy=True)
    #     client.send_message(db.get_moder(), last_id)


# @app.on_message(filters.chat(db.get_moder()))
# def send_post(client, message):
#     # получаем запись в таблице
#     for item in db.get_data_in_table(message):
#         username = item[0]
#         msg_id = item[1]

#     send = app.get_messages(username, msg_id)
#     send.forward(db.get_channel(), as_copy=True)