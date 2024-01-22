from aiogram import types
from ..config import dp
from .. import handlers
import httpx


ARTICLES = ("der", "die", "das")


def check_word_article(article: str, word: str): 
    r = httpx.get(f"https://der-artikel.de/{article}/{word}.html")

    return r.status_code == 200


def get_word_article(word: str):
    for article in ARTICLES:
        if check_word_article(article, word):
            return f"{article} **{word}**"


@dp.message_handler(commands=["den"])
@handlers.get_text
async def deutsch(message: types.Message, word: str):
    result = get_word_article(word.title())

    if result is not None:
        await message.reply(result, parse_mode="Markdown")
    else:
        await message.reply(f"Substantiv »{word}« wurde nicht gefunden.")
