from aiogram import types
from aiogram.filters import Command
from aiogram.utils.markdown import bold

from ..config import router
from ..filters import GetText
from ..lib.aioget import aioget

ARTICLES = ("der", "die", "das")


async def check_word_article(article: str, word: str) -> bool:
    r = await aioget(f"https://der-artikel.de/{article}/{word}.html")

    return r.status_code == 200


async def get_word_article(word: str) -> str:
    for article in ARTICLES:
        if await check_word_article(article, word):
            return f"{article} {bold(word)}"

    return f"Substantiv »{bold(word)}« wurde nicht gefunden"


@router.message(Command("den"), GetText(disable_reply=True))
async def deutsch(message: types.Message, query: str):
    result = await get_word_article(query.title())

    await message.reply(result)
