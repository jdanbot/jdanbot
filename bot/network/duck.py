from aiogram import types
from pyduckgo import Duck

from ..config import dp
from .. import handlers
from ..lib.text import bold, fixWords

duck = Duck()


@dp.message_handler(commands=["duck"])
@handlers.parse_arguments(1)
async def getDuck(message: types.Message, query: str):
    text = ""

    links = await duck.search(query)

    for link in links[:10]:
        link["title"] = bold(fixWords(link["title"]))
        title = f"<a href='{link['url']}'>{link['title']}</a>"

        text += title + "\n"
        text += f"{link['description']}\n\n"

    await message.reply(text, parse_mode="HTML", disable_web_page_preview=True)
