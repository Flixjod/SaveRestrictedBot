# FLiX/test.py

from pyrogram import Client, filters
from pyrogram.types import Message
from database.db import database

@Client.on_message(filters.command("test") & filters.private)
async def test(client: Client, message: Message):
    user_data = database.find_one({"user_id": message.from_user.id})
    
    if user_data is None:
        await message.reply("**You are not logged in! Please /login first.**")
        return

    await message.reply("**Test command received! You are logged in.**")
