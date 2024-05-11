from aiogram import types
from aiogram.filters import Command
from aiogram.utils.markdown import hbold
from pyduckgo import Duck

from ..config import router
from ..filters import GetText
from ..lib.text import fix_words

duck = Duck()


@router.message(Command("duck"), GetText(disable_reply=True))
async def get_duck(message: types.Message, query: str):
    text = ""

    links = await duck.search(query)

    for link in links[:10]:
        link["title"] = hbold(fix_words(link["title"]))
        title = f"<a href='{link['url']}'>{link['title']}</a>"

        text += title + "\n"
        text += f"{link['description']}\n\n"

    await message.reply(
        text, parse_mode="HTML", disable_web_page_preview=True
    )
