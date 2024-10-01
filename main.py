from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN

class Bot(Client):
    def __init__(self):
        super().__init__(
            "FLIX_savelogin",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="FLiX"),  # Load plugins from FLiX directory
            workers=50,
            sleep_threshold=10
        )

    async def start(self):
        await super().start()
        bot_info = await self.get_me()  # Get bot information
        print(f"@{bot_info.username} Bot Started Powered By @FLiX_LY")
        
        # Print all registered command handlers
        command_handlers = [handler for handler in self.handlers if handler.filters and handler.filters.command]
        print("All Command Handlers:")
        for handler in command_handlers:
            commands = handler.filters.command
            handler_name = handler.callback.__name__  # Get the name of the handler function
            for command in commands:
                print(f"- Command: {command}, Handler: {handler_name}")

    async def stop(self, *args):
        await super().stop()
        print("Bot Stopped Bye")
