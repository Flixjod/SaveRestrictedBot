from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserAlreadyParticipant, InviteHashExpired, UsernameNotOccupied
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message 
from pyrogram.enums import ChatMemberStatus
from datetime import datetime, timedelta
import os
import threading
from config import API_ID, API_HASH, OWNER_ID, FSUB_ID, FSUB_INV_LINK
from database.db import database 
from FLiX.save import is_member


@Client.on_message(filters.command(["test"]))
async def TEST(client: Client, message: Message):

    # Check if the user is a member of the required channel/group
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

	    
    if not database.users.find_one({'user_id': message.from_user.id}):
        database.users.insert_one({
            'user_id': message.from_user.id,
            'first_name': message.from_user.first_name,
            'registered_at': time.time(),
            'plan': 'free',
	    'premium_expiration': None,
            'last_download_time': None
            
            
        })
	
    buttons = [[
        InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ ⚡️", url = "https://t.me/FLiX_LY")
    ],[
        InlineKeyboardButton('🔍 sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url='https://t.me/Flix_botz'),
        InlineKeyboardButton('🤖 ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url='https://t.me/Flix_botz')
	]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_message(message.chat.id, f"<b>👋 Hi {message.from_user.mention}, I am Save Restricted Content Bot, I can send you restricted content by its post link.\n\n ✅ /login » For downloading \n\n ❌ /logout » For Logout account \n\n 💟 /help » Know how to use bot by </b>", reply_markup=reply_markup, reply_to_message_id=message.id)
    return

