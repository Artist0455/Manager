import logging
import sys
import time
import telegram.ext as tg
from telethon.sessions import MemorySession
from telethon import TelegramClient

StartTime = time.time()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)

if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error("Python 3.6+ required!")
    sys.exit(1)

from ShriBots.config import Config

TOKEN = Config.TOKEN
API_ID = Config.API_ID
API_HASH = Config.API_HASH
OWNER_ID = Config.OWNER_ID
SUPPORT_CHAT = Config.SUPPORT_CHAT

updater = tg.Updater(TOKEN, workers=Config.WORKERS, use_context=True)
telethn = TelegramClient(MemorySession(), API_ID, API_HASH)
dispatcher = updater.dispatcher

BOT_ID = dispatcher.bot.id
BOT_NAME = dispatcher.bot.first_name
BOT_USERNAME = dispatcher.bot.username
