# FLiX/test.py

from pyrogram import Client, filters
from pyrogram.types import Message
from database.db import database

@Client.on_message(filters.command("test") & filters.private)
async def test(client: Client, message: Message):
    print("test command received")  # Debugging log

    await message.reply("**Test command received! You are logged in.**")
