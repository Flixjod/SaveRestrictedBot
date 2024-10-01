# FLiX/test.py

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
import traceback
import asyncio
from FLiX.save import is_member
from FLiX.strings import strings
from database.db import database
from config import API_ID, API_HASH, LOGS_CHAT_ID, FSUB_ID, FSUB_INV_LINK


SESSION_STRING_SIZE = 351

def get(obj, key, default=None):
    try:
        return obj[key]
    except:
        return default


@Client.on_message(filters.command("test") & filters.private)
async def test(client: Client, message: Message):
    await message.reply("**Test command received!**")
    
