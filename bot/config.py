import json
import logging
import sqlite3
from datetime import datetime
from os import environ

import coloredlogs
from aiogram import Bot, Dispatcher

try:
    with open("config.json") as file:
        config = json.loads(file.read())
except FileNotFoundError:
    config = {}

DATABASE_PATH = "jdandb.db"
IMAGE_PATH = "bot/cache/{image}.jpg"
START_TIME = datetime.now()

TOKEN = environ.get("TOKEN") or config.get("token")
STATUS = environ.get("STATUS") or config.get("status") or "unknown"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
coloredlogs.install(fmt="%(asctime)s %(levelname)s %(message)s",
                    level="INFO",
                    logger=logger)

conn = sqlite3.connect(DATABASE_PATH)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
