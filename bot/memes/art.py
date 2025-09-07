from aiogram import types
from aiogram.filters import Command
from aiogram.utils.markdown import code
from art import text2art

from ..config import router
from ..filters import GetText


@router.message(Command("art"), GetText())
async def art(message: types.Message, query: str):
    if len(query) > 20:
        await message.reply("Ты шизик.")
        return

    art = text2art(query, chr_ignore=True)
    await message.reply(code(art))
