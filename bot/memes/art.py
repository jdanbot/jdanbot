from aiogram import types
from aiogram.filters import Command
from aiogram.utils.markdown import code
from stripped import text2art

from ..config import router
from ..config.lib.locales import Locale
from ..filters import GetText


@router.message(Command("art", "art2"), GetText())
async def art(
    message: types.Message, query: str, _: Locale
):
    if len(query) > 20:
        await message.reply("Ты шизик.")
        return

    enable_cyrillic = message.text.startswith("/art ")
    art = text2art(query, enable_cyrillic)

    await message.reply(
        code(art) if art != "" else _.errors.no_symbols
    )
