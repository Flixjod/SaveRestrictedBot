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
        
        print("All Command Handlers:")
        for group_key, group_handlers in self.dispatcher.groups.items():
            for handler in group_handlers:
                # Ensure handler has 'filters' and 'commands' attributes
                if hasattr(handler, 'filters') and isinstance(handler.filters, filters.Command):
                    commands = handler.filters.commands  # Get list of commands
                    handler_name = handler.callback.__name__  # Get handler function name
                    for command in commands:
                        print(f"- Command: {command}, Handler: {handler_name}")


    async def stop(self, *args):
        await super().stop()
        print("Bot Stopped. Alvida!")  # Updated stop message
