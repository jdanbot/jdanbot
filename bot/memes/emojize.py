import random

from aiogram import types
from aiogram.filters import Command
from stripped.emoji import EMOJI

from ..config import router
from ..filters import GetText


@router.message(Command("emojize"), GetText())
async def emojize(message: types.Message, query: str):
    text = ""

    for word in query.split(" "):
        emoji = random.choice(EMOJI)
        text += emoji + word

    await message.reply(text, parse_mode=None)
