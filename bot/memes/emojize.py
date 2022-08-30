from aiogram import types

from ..config import dp
from .. import handlers

from emoji import EMOJI_DATA

import random


emoji_list = list(set([emoji[0] for emoji in EMOJI_DATA if EMOJI_DATA[emoji]["status"] == 2]))


@dp.message_handler(commands=["emojize"])
@handlers.get_text
async def emojize(message: types.Message, query: str):
    text = ""

    for word in query.split(" "):
        emoji = random.choice(emoji_list)
        text += emoji + word

    await message.reply(text)
