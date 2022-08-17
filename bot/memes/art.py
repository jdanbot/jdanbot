from aiogram import types
from art import text2art

from ..config import dp
from .. import handlers
from ..lib.text import code


@dp.message_handler(commands=["art"])
@handlers.get_text
async def art(message: types.Message, text: str):
    if len(text) > 20:
        await message.reply("Ты шизик.")
        return

    art = text2art(text, chr_ignore=True)
    await message.reply(code(art), parse_mode="HTML")
