import coloredlogs
import logging
import sqlite3
import json

from os import environ
from datetime import datetime
from aiogram import Bot, Dispatcher


if "TOKEN" in environ:
    TOKEN = environ["TOKEN"]

    try:
        bot_status = environ["STATUS"]
    except:
        print("Enter status of bot in token.json")
else:
    try:
        with open("config.json") as file:
            config = json.loads(file.read())
            TOKEN = config["token"]

            try:
                bot_status = config["status"]
            except KeyError:
                print("Enter status of bot in token.json")
                bot_status = "unknown"

    except:
        print("Create config.json with bot token")
        exit()

start_time = datetime.now()
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
coloredlogs.install(fmt="%(asctime)s %(levelname)s %(message)s",
                    level="INFO",
                    logger=logger)
log = logger.info

conn = sqlite3.connect("jdandb.db")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
