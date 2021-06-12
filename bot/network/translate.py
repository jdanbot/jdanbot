from googletrans import Translator
from ..config import dp, bot, _, GTRANSLATE_LANGS
from ..lib import handlers

from random import choice

t = Translator()


@dp.message_handler(commands=["tru"])
@handlers.get_text
async def tru(message, text):
    await message.reply(t.translate(text, dest="ru").text[:4096],
                        disable_web_page_preview=True)


@dp.message_handler(commands=["ten"])
@handlers.get_text
async def tru(message, text):
    await message.reply(t.translate(text, dest="en").text[:4096],
                        disable_web_page_preview=True)


@dp.message_handler(commands=["tuk", "tua"])
@handlers.get_text
async def tru(message, text):
    await message.reply(t.translate(text, dest="ua").text[:4096],
                        disable_web_page_preview=True)


@dp.message_handler(commands=["tbe", "tby"])
@handlers.get_text
async def tru(message, text):
    await message.reply(t.translate(text, dest="be").text[:4096],
                        disable_web_page_preview=True)


@dp.message_handler(commands=["tpl"])
@handlers.get_text
async def tru(message, text):
    await message.reply(t.translate(text, dest="pl").text[:4096],
                        disable_web_page_preview=True)


@dp.message_handler(commands=["tde"])
@handlers.get_text
async def tru(message, text):
    await message.reply(t.translate(text, dest="de").text[:4096],
                        disable_web_page_preview=True)


@dp.message_handler(commands=["crazy"])
@handlers.get_text
async def crazy_translator(message, text):
    for _ in range(0, 10):
        text = t.translate(text, dest=choice(GTRANSLATE_LANGS)).text

    await message.reply(t.translate(text, dest="ru").text)
