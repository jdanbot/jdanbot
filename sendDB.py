import logging
import json

import asyncio
from os import environ
from aiogram import Bot, Dispatcher

if "TOKEN" in environ:
    TOKEN = environ["TOKEN"]

else:
    with open("token.json") as file:
        token = json.loads(file.read())
        TOKEN = token["token"]

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


async def main():
    await bot.send_document(795449748, document=open("jdanbot.db", "rb"))

asyncio.run(main())
