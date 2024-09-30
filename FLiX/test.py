import asyncio 
import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserAlreadyParticipant, InviteHashExpired, UsernameNotOccupied
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message 
from pyrogram.enums import ChatMemberStatus
import time
import pytz
from datetime import datetime, timedelta
import os
import threading
import json
from config import API_ID, API_HASH, OWNER_ID, FSUB_ID, FSUB_INV_LINK
from database.db import database 
from FLiX.strings import strings, HELP_TXT


def get(obj, key, default=None):
    try:
        return obj[key]
    except:
        return default
	    

async def is_member(client: Client, user_id: int) -> bool:
    try:
        # Get the chat member information
        chat_member = await client.get_chat_member(FSUB_ID, user_id)
      
        # Check if the user is a member, administrator, or creator
        return chat_member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False



@Client.on_message(filters.command("test") & filters.private)
async def test(client: Client, message: Message):
    if not await is_member(client, message.from_user.id):
        
        await client.send_message(
            chat_id=message.chat.id,
            text=f"👋 ʜɪ {message.from_user.mention}, ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴍʏ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴍᴇ.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("ᴊᴏɪɴ ❤️", url=FSUB_INV_LINK)
            ]]),
            reply_to_message_id=message.id  
        )
        return
        
    user_data = database.sessions.find_one({"user_id": message.chat.id})
    if user_data is None or not user_data.get('logged_in', False):
        await message.reply("**You are not logged in! Please /login first.**")
        return
    data = {
        'logged_in': False,
        'session': None,
        '2FA': None
    }
    database.sessions.update_one({'_id': user_data['_id']}, {'$set': data})
    await message.reply("**Logout Successfully** ♦")
	
