from pyrogram import Client
import os
import logging
from config import API_ID, API_HASH, BOT_TOKEN

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize the bot client with custom parameters
bot = Client(
    "FLIX_savelogin",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins={'root': 'FLiX'},  # Specify the root directory for plugins
    workers=50,  # Number of workers for handling requests
    sleep_threshold=10  # Threshold for sleeping between requests
)

# Load plugins from the FLiX folder
plugins_path = "FLiX"
for filename in os.listdir(plugins_path):
    if filename.endswith(".py") and filename != "__init__.py":
        try:
            bot.load_plugin(f"{plugins_path}.{filename[:-3]}")  # Load plugin without .py extension
            logging.info(f"Loaded plugin: {filename}")
        except Exception as e:
            logging.error(f"Error loading plugin {filename}: {e}")

# Start the bot
@bot.on_start()
async def on_start(client):
    logging.info("Bot Started Powered By @FLiX_LY")  # Update startup message

# Handle bot shutdown
@bot.on_shutdown()
async def on_shutdown(client):
    logging.info("Alvida! The bot is shutting down.")

# Run the bot
if __name__ == "__main__":
    bot.run()
