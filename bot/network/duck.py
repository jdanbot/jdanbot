from ..lib.fixWords import fixWords
from ..lib.html import bold
from ..data import data
from ..config import dp

from pyduckgo import Duck


duck = Duck()


@dp.message_handler(commands=["duck"])
async def getDuck(message):
    opts = message.text.split(maxsplit=1)
    if len(opts) == 1:
        await message.reply(data["duckerror"].format(opts[0]),
                            parse_mode="Markdown")
        return

    query = opts[1]
    text = ""

    links = await duck.HTML_search(query)

    for link in links[:10]:
        url = "https:{url}".format(url=link["url"])
        link["title"] = bold(fixWords(link["title"]))
        title = "<a href='{url}'>{title}</a>".format(title=link["title"],
                                                     url=url)

        text += title + "\n"
        text += f"{link['description']}\n\n"

    await message.reply(text, parse_mode="HTML", disable_web_page_preview=True)
