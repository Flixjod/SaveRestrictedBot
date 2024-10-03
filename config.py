import os

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
FSUB_ID = int(os.environ.get("FSUB_ID", ""))
if FSUB_ID:
    FSUB_ID = int(FSUB_ID)  # Convert to int if it's not empty
else:
    FSUB_ID = None  # Set to None if FSUB_ID is not set

#Force Sub Channel Invite Link
FSUB_INV_LINK = os.environ.get("FSUB_INV_LINK", "")
