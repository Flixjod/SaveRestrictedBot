# Don't Remove Credit Tg - @FLiX_LY
# Ask Doubt on telegram @FLiX_LY

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

def Check_Plan(user_id):
    user_data = database.users.find_one({'user_id': user_id})
    
    # If the user is not found or doesn't have a 'plan', they are considered free users
    if not user_data or user_data.get('plan') != 'premium':
        return True
    
    # Check if the premium expiration date has passed
    premium_expiration = user_data.get('premium_expiration')
    if premium_expiration and datetime.utcnow() > premium_expiration:
        # If expired, downgrade to free and return True
        database.users.update_one(
            {'user_id': user_id},
            {'$set': {'plan': 'free'}, 'premium_expiration': None}
        )
        return True
    
    # If the user is premium and the plan is still valid, they are not a free user
    return False


# Store download time after successful download
def update_last_download_time(user_id: int):
    database.users.update_one(
        {'user_id': user_id},
        {'$set': {'last_download_time': time.time()}}
    )

def can_download(user_id: int):
    user = database.users.find_one({'user_id': user_id})
    if user:
        last_download_time = user.get('last_download_time')
        if last_download_time:
            elapsed_time = time.time() - last_download_time
            remaining_time = 300 - elapsed_time  # 5 minutes cooldown
            if remaining_time > 0:
                return False, remaining_time
        else:
            # If last_download_time is None, the user can download
            return True, 0
    # If user is not found, assume they can download
    return True, 0


async def downstatus(client: Client, statusfile, message):
    while True:
        if os.path.exists(statusfile):
            break

        await asyncio.sleep(3)
      
    while os.path.exists(statusfile):
        with open(statusfile, "r") as downread:
            txt = downread.read()
        try:
            await client.edit_message_text(message.chat.id, message.id, f"Downloaded : {txt}")
            await asyncio.sleep(10)
        except:
            await asyncio.sleep(5)


# upload status
async def upstatus(client: Client, statusfile, message):
    while True:
        if os.path.exists(statusfile):
            break

        await asyncio.sleep(3)      
    while os.path.exists(statusfile):
        with open(statusfile, "r") as upread:
            txt = upread.read()
        try:
            await client.edit_message_text(message.chat.id, message.id, f"Uploaded : {txt}")
            await asyncio.sleep(10)
        except:
            await asyncio.sleep(5)


# progress writer
def progress(current, total, message, type):
    with open(f'{message.id}{type}status.txt', "w") as fileup:
        fileup.write(f"{current * 100 / total:.1f}%")


# start command
@Client.on_message(filters.command(["start"]))
async def send_start(client: Client, message: Message):

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
    await client.send_message(message.chat.id, f"<b>👋 Hi {message.from_user.mention}, I am Save Restricted Content Bot, I can send you restricted content by its post link.\n\n ✅ /login » For downloading \n\n ❌ /logout » For Logout account \n\n⏱️ /myplan » Know Your Plan Info \n\n💟 /help » Know how to use bot by </b>", reply_markup=reply_markup, reply_to_message_id=message.id)
    return


# help command
@Client.on_message(filters.command(["help"]))
async def send_help(client: Client, message: Message):
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
	
    await client.send_message(message.chat.id, f"{HELP_TXT}")


@Client.on_message(filters.command("upgrade") & filters.private)
async def upgrade_to_premium(client, message):
    try:
        # Check if the user is an admin
        if message.from_user.id not in OWNER_ID:
            await message.reply("**❌ This command can only be used by admins.**")
            return

        # Extract user ID and days from the command
        command = message.text.split()
        if len(command) != 3:
            await message.reply("**Usage: /upgrade user_id days**")
            return
		
        # Validate user_id and days as integers
        user_id = int(command[1])
        days = int(command[2])

        # Check if the user exists in the database
        user = database.users.find_one({'user_id': user_id})
        if user is None:
            await message.reply(f"**❌ User ID {user_id} not found in the database.**")
            return

        # Fetch user details for mention
        user_info = await client.get_users(user_id)

        # Calculate premium expiration date
        current_time = datetime.utcnow()
        expiration_date = current_time + timedelta(days=days)

        # Extend expiration if already premium
        if user.get('plan') == 'premium' and user.get('premium_expiration'):
            existing_expiration = user['premium_expiration']
            if existing_expiration > current_time:
                expiration_date = existing_expiration + timedelta(days=days)

        # Convert to Indian Time Zone
        ist_timezone = pytz.timezone('Asia/Kolkata')
        current_time_ist = current_time.astimezone(ist_timezone)
        expiration_date_ist = expiration_date.astimezone(ist_timezone)

        # Format dates
        expiry_str_in_ist = expiration_date_ist.strftime('%Y-%m-%d %H:%M:%S')
        current_time_str = current_time_ist.strftime('%Y-%m-%d %H:%M:%S')

        # Update user plan in the database
        database.users.update_one(
            {'user_id': user_id},
            {'$set': {'plan': 'premium', 'premium_expiration': expiration_date}},
            upsert=True
        )

        # Notify admin
        await message.reply_text(
            f"**Premium added successfully ✅**\n\n"
            f"👤 **User:** [{user_info.first_name}](tg://user?id={user_info.id})\n"
            f"⚡ **User ID:** `{user_id}`\n"
            f"⏰ **Premium Access:** {days} days\n\n"
            f"⏳ **Joining Date:** {current_time_str}\n"
            f"⌛️ **Expiry Date:** {expiry_str_in_ist}", 
            disable_web_page_preview=True
	)
        
        # Notify the user
        await client.send_message(
            user_id,
            f"👋 Hi [{user_info.first_name}](tg://user?id={user_info.id}),\n"
            f"**Thank you for purchasing premium.\nEnjoy!** ✨🎉\n\n"
            f"⏰ **Premium Access:** {days} days\n"
            f"⏳ **Joining Date:** {current_time_str}\n"
            f"⌛️ **Expiry Date:** {expiry_str_in_ist}",
            disable_web_page_preview=True
        )

    except ValueError:
        await message.reply("**Invalid input. User ID and days must be numbers.**")
    except Exception as e:
        await message.reply(f"**An error occurred:** {e}")


@Client.on_message(filters.command("myplan") & filters.private)
async def check_plan(client: Client, message: Message):
    user_id = message.from_user.id

    # Check if the user is in the database
    user_data = database.users.find_one({'user_id': user_id})

    if not user_data:
        await message.reply("**❌ You are not registered. Please use /start to register.**")
        return

    # Get the plan and expiration details
    plan = user_data.get('plan', 'free')
    premium_expiration = user_data.get('premium_expiration')

    if plan == 'free':
        response = "Your current plan is **Free**.\n\nYou can upgrade to premium for additional features."
    else:
        if premium_expiration:
            expiration_date = premium_expiration.strftime('%Y-%m-%d %H:%M:%S')
            response = f"Your current plan is **Premium**.\n\n⏳ **Expiry Date:** {expiration_date} (UTC)"
        else:
            response = "Your current plan is **Premium**, but the expiration date is not set."

    await message.reply(response)


@Client.on_message(filters.command("remove") & filters.private)
async def remove_premium(client, message):
    try:
        # Check if the user is an admin
        if message.from_user.id not in OWNER_ID:
            await message.reply("**❌ This command can only be used by admins.**")
            return

        # Extract user ID from the command
        command = message.text.split()
        if len(command) != 2:
            await message.reply("**Usage: /remove user_id**")
            return

        # Validate user_id as an integer
        user_id = command[1]
        if not user_id.isdigit():
            await message.reply("**Invalid input. User ID must be a valid number.**")
            return

        user_id = int(user_id)  # Convert user_id to integer after validation

        # Check if the user exists in the database
        user = database.users.find_one({'user_id': user_id})
        if user is None:
            await message.reply(f"**❌ User ID {user_id} not found in the database.**")
            return

        # Fetch user details for mention
        user_info = await client.get_users(user_id)

        # Update user plan to "free" and set premium_expiration to None
        database.users.update_one(
            {'user_id': user_id},
            {'$set': {'plan': 'free', 'premium_expiration': None}}
        )

        # Notify admin
        await message.reply_text(
            f"**Premium removed successfully ✅**\n\n"
            f"👤 **User:** [{user_info.first_name}](tg://user?id={user_info.id})\n"
            f"⚡ **User ID:** `{user_id}`\n\n"
            f"**User is now on the free plan.**", 
            disable_web_page_preview=True
        )
        
        # Notify the user
        await client.send_message(
            user_id,
            f"👋 Hi [{user_info.first_name}](tg://user?id={user_info.id}),\n"
            f"**Your premium plan has been removed.**\n"
            f"**You are now on the free plan.**",
            disable_web_page_preview=True
        )

    except Exception as e:
        await message.reply(f"**An error occurred:** {e}")



@Client.on_message(filters.text & filters.private)
async def save(client: Client, message: Message):
    
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

	
    if Check_Plan(message.from_user.id):
        can_download_now, remaining_time = can_download(message.from_user.id)
        if not can_download_now:
            # Convert remaining time to minutes and seconds
            remaining_minutes, remaining_seconds = divmod(remaining_time, 60)
            await client.send_message(
                chat_id=message.chat.id,
                text=f"**❌ Free User Can Save Single File in Every 5min Please wait {int(remaining_minutes)} Min and {int(remaining_seconds)} Sec before trying again.\n\nIf You Dont Want To Wait Then Buy Premium**",
		reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ ⚡️", url="https://t.me/FLiX_LY")
                ]]),
                reply_to_message_id=message.id
            )
            return

	
    if "https://t.me/" in message.text:
        datas = message.text.split("/")
        temp = datas[-1].replace("?single","").split("-")
        fromID = int(temp[0].strip())
        try:
            toID = int(temp[1].strip())
        except:
            toID = fromID

        # If the user is free and there's a range (fromID-toID), restrict them
        if Check_Plan(message.from_user.id) and fromID != toID:
            await client.send_message(
                chat_id=message.chat.id,
                text="**❌ Free Users Can Only Save Single File at a Time, If You Want To Save Bulk File Then Buy Premium**",
		reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ ⚡️", url="https://t.me/FLiX_LY")
                ]]),
                reply_to_message_id=message.id
            )
            return

        
        for msgid in range(fromID, toID + 1):
            
            # Update last download time for free users
            if Check_Plan(message.from_user.id):
                update_last_download_time(message.from_user.id)

            # Private
            if "https://t.me/c/" in message.text:
                user_data = database.sessions.find_one({'user_id': message.from_user.id})
                if not get(user_data, 'logged_in', False) or user_data['session'] is None:
                    await client.send_message(message.chat.id, strings['need_login'])
		    
                    database.users.update_one({'user_id': message.from_user.id}, {'$set': {'last_download_time': None}})
                    return
                acc = Client("saverestricted", session_string=user_data['session'], api_hash=API_HASH, api_id=API_ID)
                await acc.connect()
                chatid = int("-100" + datas[4])
                await handle_private(client, acc, message, chatid, msgid)
    
            # bot
            elif "https://t.me/b/" in message.text:
                user_data = database.find_one({"user_id": message.from_user.id})
                if not get(user_data, 'logged_in', False) or user_data['session'] is None:
                    await client.send_message(message.chat.id, strings['need_login'])
		    
                    database.users.update_one({'user_id': message.from_user.id}, {'$set': {'last_download_time': None}})
                    return
                acc = Client("saverestricted", session_string=user_data['session'], api_hash=API_HASH, api_id=API_ID)
                await acc.connect()
                username = datas[4]
                try:
                    await handle_private(client, acc, message, username, msgid)
                except Exception as e:
                    await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)
            
	        # public
            else:
                username = datas[3]

                try:
                    msg = await client.get_messages(username, msgid)
                except UsernameNotOccupied: 
                    await client.send_message(message.chat.id, "The username is not occupied by anyone", reply_to_message_id=message.id)
                    return
                try:
                    await client.copy_message(message.chat.id, msg.chat.id, msg.id, reply_to_message_id=message.id)
                except:
                    try:    
                        user_data = database.find_one({"user_id": message.from_user.id})
                        if not get(user_data, 'logged_in', False) or user_data['session'] is None:
                            await client.send_message(message.chat.id, strings['need_login'])
                            
                            database.users.update_one({'user_id': message.from_user.id}, {'$set': {'last_download_time': None}})
                            return
                        acc = Client("saverestricted", session_string=user_data['session'], api_hash=API_HASH, api_id=API_ID)
                        await acc.connect()
                        await handle_private(client, acc, message, username, msgid)
                        
                    except Exception as e:
                        await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)
                        
                        database.users.update_one({'user_id': message.from_user.id}, {'$set': {'last_download_time': None}})

            # wait time
            await asyncio.sleep(3)


# handle private
async def handle_private(client: Client, acc, message: Message, chatid: int, msgid: int):
    msg: Message = await acc.get_messages(chatid, msgid)
    msg_type = get_message_type(msg)
    chat = message.chat.id
    if "Text" == msg_type:
        try:
            await client.send_message(chat, msg.text, entities=msg.entities, reply_to_message_id=message.id)
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)
	        
            # Set last_download_time to None in case of an error
            database.users.update_one({'user_id': message.from_user.id}, {'$set': {'last_download_time': None}})
            return

    smsg = await client.send_message(message.chat.id, 'Downloading', reply_to_message_id=message.id)
    dosta = asyncio.create_task(downstatus(client, f'{message.id}downstatus.txt', smsg))
    try:
        file = await acc.download_media(msg, progress=progress, progress_args=[message,"down"])
        os.remove(f'{message.id}downstatus.txt')
        
    except Exception as e:
        await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)  
	    
        # Set last_download_time to None in case of an error
        database.users.update_one({'user_id': message.from_user.id}, {'$set': {'last_download_time': None}})
        
    
    upsta = asyncio.create_task(upstatus(client, f'{message.id}upstatus.txt', smsg))

    if msg.caption:
        caption = msg.caption
    else:
        caption = None
            
    if "Document" == msg_type:
        try:
            ph_path = await acc.download_media(msg.document.thumbs[0].file_id)
        except:
            ph_path = None
        
        try:
            await client.send_document(chat, file, thumb=ph_path, caption=caption, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)
            
            # Set last_download_time to None in case of an error
            database.users.update_one({'user_id': message.from_user.id}, {'$set': {'last_download_time': None}})
        if ph_path != None: os.remove(ph_path)
        

    elif "Video" == msg_type:
        try:
            ph_path = await acc.download_media(msg.video.thumbs[0].file_id)
        except:
            ph_path = None
        
        try:
            await client.send_video(chat, file, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, thumb=ph_path, caption=caption, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)

            # Set last_download_time to None in case of an error
            database.users.update_one({'user_id': message.from_user.id}, {'$set': {'last_download_time': None}})
        if ph_path != None: os.remove(ph_path)

    elif "Animation" == msg_type:
        try:
            await client.send_animation(chat, file, reply_to_message_id=message.id)
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)
            
            # Set last_download_time to None in case of an error
            database.users.update_one({'user_id': message.from_user.id}, {'$set': {'last_download_time': None}})
        
        

    elif "Sticker" == msg_type:
        try:
            await client.send_sticker(chat, file, reply_to_message_id=message.id)
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)

            # Set last_download_time to None in case of an error
            database.users.update_one({'user_id': message.from_user.id}, {'$set': {'last_download_time': None}})
        

    elif "Voice" == msg_type:
        try:
            await client.send_voice(chat, file, caption=caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)
            
            # Set last_download_time to None in case of an error
            database.users.update_one({'user_id': message.from_user.id}, {'$set': {'last_download_time': None}})


    elif "Audio" == msg_type:
        try:
            ph_path = await acc.download_media(msg.audio.thumbs[0].file_id)
        except:
            ph_path = None

        try:
            await client.send_audio(chat, file, thumb=ph_path, caption=caption, reply_to_message_id=message.id, progress=progress, progress_args=[message,"up"])   
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)

            # Set last_download_time to None in case of an error
            database.users.update_one({'user_id': message.from_user.id}, {'$set': {'last_download_time': None}})
        
        if ph_path != None: os.remove(ph_path)

    elif "Photo" == msg_type:
        try:
            await client.send_photo(chat, file, caption=caption, reply_to_message_id=message.id)
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)

            # Set last_download_time to None in case of an error
            database.users.update_one({'user_id': message.from_user.id}, {'$set': {'last_download_time': None}})
    
    if Check_Plan(message.from_user.id):
            update_last_download_time(message.from_user.id)

	
    if os.path.exists(f'{message.id}upstatus.txt'): 
        os.remove(f'{message.id}upstatus.txt')
        os.remove(file)
    await client.delete_messages(message.chat.id,[smsg.id])



# get the type of message
def get_message_type(msg: pyrogram.types.messages_and_media.message.Message):
    try:
        msg.document.file_id
        return "Document"
    except:
        pass

    try:
        msg.video.file_id
        return "Video"
    except:
        pass

    try:
        msg.animation.file_id
        return "Animation"
    except:
        pass

    try:
        msg.sticker.file_id
        return "Sticker"
    except:
        pass

    try:
        msg.voice.file_id
        return "Voice"
    except:
        pass

    try:
        msg.audio.file_id
        return "Audio"
    except:
        pass

    try:
        msg.photo.file_id
        return "Photo"
    except:
        pass

    try:
        msg.text
        return "Text"
    except:
        pass
