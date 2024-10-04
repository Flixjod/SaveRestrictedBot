import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

#Bot token @Botfather
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

#Your API ID from my.telegram.org
API_ID = int(os.environ.get("API_ID", ""))

#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "")

# OWNER IDs
OWNER_ID = list(map(int, os.environ.get("OWNER_ID", "").split(",")))

#Database 
DB_URI = os.environ.get("DB_URI", "")

#Your Logs Channel/Group ID
LOGS_CHAT_ID = int(os.environ.get("LOGS_CHAT_ID", ""))

#Force Sub Channel ID
FSUB_ID = int(os.environ.get("FSUB_ID", "") or 0) or None

#Force Sub Channel Invite Link
FSUB_INV_LINK = os.environ.get("FSUB_INV_LINK", "")
