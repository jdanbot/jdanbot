import logging
import json

from os import environ
from aiogram import Bot, Dispatcher


if "TOKEN" in environ:
    TOKEN = environ["TOKEN"]
    heroku = True

else:
    with open("bot/token.json") as token:
        TOKEN = json.loads(token.read())["token"]
        heroku = False


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
