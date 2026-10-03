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

    results = await duck.search(query)

    for res in results[:10]:
        fixed_title = hbold(fix_words(res.title))
        title = f"<a href='{res.link}'>{fixed_title}</a>"

        text += title + "\n"
        text += f"{res.snippet}\n\n"

    await message.reply(
        text, parse_mode="HTML", disable_web_page_preview=True
    )
