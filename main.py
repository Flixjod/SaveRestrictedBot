from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN

class Bot(Client):
    def __init__(self):
        super().__init__(
            "FLIX_savelogin",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="FLiX"),
            workers=50,
            sleep_threshold=10
        )

    async def start(self):
        await super().start()
        bot_info = await self.get_me()  # Get bot information
        print(f"@{bot_info.username} Is Started Powered By @FLiX_LY")
        
        
    async def stop(self, *args):
        await super().stop()
        print("Bot Stopped. Alvida!")  # Updated stop message
