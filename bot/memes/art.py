from aiogram import types
from art import text2art

from aiogram.filters import Command
from ..config import router
from ..filters import GetText
from aiogram.utils.markdown import code


@router.message(Command("art"), GetText())
async def art(message: types.Message, query: str):
    if len(query) > 20:
        await message.reply("Ты шизик.")
        return

    art = text2art(query, chr_ignore=True)
    await message.reply(code(art))
