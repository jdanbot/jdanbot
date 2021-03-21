import aiosqlite
import coloredlogs
import yaml
from aiogram import Bot, Dispatcher
from aiovk import TokenSession, API
from pytz import timezone

import asyncio
import logging
import traceback
from datetime import datetime
from os import environ
from .lib.text import code
from .lib.driver import HttpDriver
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
config.get("rss", default=False)
config.get("image_path", default="bot/cache/{image}.jpg")
config.get("token")
config.get("status", default="unknown")
config.get("vk", default=False)
config.get("vk_channels")
config.get("access_token")

SCHEDULE = VK or RSS

START_TIME = datetime.now()
TIMEZONE = timezone("Europe/Moscow")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
coloredlogs.install(fmt="%(asctime)s %(levelname)s %(message)s",
                    level="INFO",
                    logger=logger)


class ResendLogs(logging.Filter):
    def filter(self, record):
        loop = asyncio.get_event_loop()
        tsk = loop.create_task(self.send_to_tg(record))
        return True

    async def send_to_tg(self, record):
        await bot.send_message(-1001435542296, code(record.msg),
                               parse_mode="HTML")


logging.getLogger("schedule").addFilter(NoRunningJobFilter())
logging.getLogger("asyncio").addFilter(ResendLogs())


async def connect_db():
    return await aiosqlite.connect(DB_PATH)


conn = asyncio.run(connect_db())

# loop = asyncio.new_event_loop()
driver = HttpDriver()

session = TokenSession(access_token=ACCESS_TOKEN, driver=driver)
vk_api = API(session)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
