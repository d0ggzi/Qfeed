from pyrogram import Client, filters
from pyrogram.types import Message
from parser import db
from config import settings


app = Client('bot_python', settings.API_ID, settings.API_HASH)


@app.on_message(filters.chat(db.get_channels()))
async def get_post(client, message: Message):
    await message.forward(settings.BOT_ID)
