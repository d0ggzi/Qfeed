from pyrogram import Client, filters
from datetime import datetime
import os
import sys
base_dir = os.path.abspath(os.path.join(os.path.dirname('main.py'), '..'))
sys.path.append(base_dir)
from sql import SQL
import config

app = Client('bot_python', config.API_ID, config.API_HASH)
db = SQL()


# @app.on_message(filters.chat(db.get_channels()))
# def get_post(client, message):
#     username = message.chat.username
#     message_id = message.message_id

#     if not db.message_id_exists(username, message_id):
#         db.add_message_id(username, message_id)
#         # получение последнего ROWID
#         for a in db.get_last_rowid():
#             last_id = a[0]

#         # перессылка поста на модерку
#         message.forward(db.get_moder(), as_copy=True)
#         client.send_message(db.get_moder(), last_id)


# @app.on_message(filters.chat(db.get_moder()))
# def send_post(client, message):
#     # получаем запись в таблице
#     for item in db.get_data_in_table(message):
#         username = item[0]
#         msg_id = item[1]

#     send = app.get_messages(username, msg_id)
#     send.forward(db.get_channel(), as_copy=True)


if __name__ == '__main__':
    print(datetime.today().strftime(f'%H:%M:%S | Bot Telegram-Grabber launched.'))
    app.run()