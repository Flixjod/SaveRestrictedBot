# Don't Remove Credit Tg - @FLiX_LY
# Ask Doubt on telegram @FLiX_LY


import logging
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Bot(Client):

    def __init__(self):
        super().__init__(
            "FLIX_savelogin",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins={'root': 'FLiX'},
            workers=50,
            sleep_threshold=10
        )

    async def start(self):
        try:
            await super().start()
            logger.info('Bot Started Powered By @FLiX_LY')
        except Exception as e:
            logger.error(f"Error starting bot: {e}")

    async def stop(self, *args):
        try:
            await super().stop()
            logger.info('Bot Stopped Bye')
        except Exception as e:
            logger.error(f"Error stopping bot: {e}")

# Example of running the bot
if __name__ == "__main__":
    bot = Bot()
    bot.run()


# Don't Remove Credit Tg - @FLiX_LY
# Ask Doubt on telegram @FLiX_LY
