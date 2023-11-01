from pyrogram import Client, filters
from pyrogram.types import Message

app = Client('bot_python', '1604211', 'f50d058743bc5f24d62e14e41dc8ddcd')

chats = [('-1001414693404',), ('-1001122357347',), ('-1001834059901',), ('-1001726580231',), ('-1001099505434',), ('-1001522226032',), ('-1001009080052',), ('-1001135818819',)]
chats2 = [-1001414693404, -1001122357347, -1001834059901]
#db.get_channels()
@app.on_message(filters.chat(chats2))
async def get_post(client, message: Message):

    print(message)

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


if __name__ == '__main__':
    app.run()