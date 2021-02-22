from ..config import dp
from ..lib import handlers


@dp.message_handler(commands=["title"])
@handlers.get_text
async def title(message, text):
    await message.reply(text.title())


@dp.message_handler(commands=["upper"])
@handlers.get_text
async def upper(message, text):
    await message.reply(text.upper())


@dp.message_handler(commands=["lower"])
@handlers.get_text
async def lower(message, text):
    await message.reply(text.lower())


@dp.message_handler(commands=["markdown"])
@handlers.get_text
async def markdown(message, text):
    await message.reply(text, parse_mode="Markdown")
