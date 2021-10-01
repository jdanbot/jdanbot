from pyduckgo import Duck

from ..config import dp
from ..lib import handlers
from ..lib.text import bold, fixWords

duck = Duck()


@dp.message_handler(commands=["duck"])
@handlers.parse_arguments(2)
async def getDuck(message, params):
    query = params[1]
    text = ""

    links = await duck.search(query)

    for link in links[:10]:
        link["title"] = bold(fixWords(link["title"]))
        title = f"<a href='{link['url']}'>{link['title']}</a>"

        text += title + "\n"
        text += f"{link['description']}\n\n"

    await message.reply(text, parse_mode="HTML", disable_web_page_preview=True)
