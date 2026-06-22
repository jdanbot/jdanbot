import random

from aiogram import types
from aiogram.filters import Command
from emoji import EMOJI_DATA

from ..config import router
from ..filters import GetText

emoji_list = [
    emoji[0]
    for emoji in EMOJI_DATA
    if EMOJI_DATA[emoji]["status"] == 2
]


@router.message(Command("emojize"), GetText())
async def emojize(message: types.Message, query: str):
    text = ""

    for word in query.split(" "):
        emoji = random.choice(emoji_list)
        text += emoji + word

    await message.reply(text, parse_mode=None)
