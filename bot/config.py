import aiosqlite
import coloredlogs
import yaml
from aiogram import Bot, Dispatcher

import asyncio
import logging
from datetime import datetime
from os import environ
from .lib.filters import NoRunningJobFilter


class Config:
    def __init__(self, file_path="config.yml"):
        with open(file_path, encoding="UTF-8") as file:
            self.config = yaml.full_load(file.read())

        self.environ = environ

    def get(self, param, default=None):
        globals()[param.upper()] = self.config.get(param) or \
                                   self.environ.get(param.upper()) or \
                                   default


config = Config()
config.get("db_path", default="jdanbot.db")
config.get("delay", default=30)
config.get("rss_feeds", default=[])
config.get("rss")
config.get("image_path", default="bot/cache/{image}.jpg")
config.get("token")
config.get("status", default="unknown")

START_TIME = datetime.now()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
coloredlogs.install(fmt="%(asctime)s %(levelname)s %(message)s",
                    level="INFO",
                    logger=logger)

logging.getLogger("schedule").addFilter(NoRunningJobFilter())


async def connect_db():
    return await aiosqlite.connect(DB_PATH)


conn = asyncio.run(connect_db())

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
