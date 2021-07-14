from bs4 import BeautifulSoup
from ..lib.aioget import aioget
from tghtml import TgHTML

from ..config import dp, _
from ..lib import handlers
from ..lib.text import bold, cuteCrop


@dp.message_handler(commands="scp")
@handlers.parse_arguments(2)
async def scp(message, params):
    query = params[1]

    search = await aioget(f"http://scp-ru.wikidot.com/search:site/q/{query}")
    soup = BeautifulSoup(search.text, "lxml")
    search_box = soup.find("div", {"id": "page-content"})

    search_items = []

    for item in search_box.find_all("div", {"class": "item"}):
        search_items.append({
            "title": item.find("div", class_="title").a.text.strip(),
            "description": item.find("div", class_="preview").text.strip(),
            "url": item.find("div", class_="url").text.strip()
        })


    def get_scp_number(q):
        title = q["title"].split(" - ", maxsplit=1)

        if len(title) == 1:
            return 9999999999999
        else:
            return int(title[0].split("-", maxsplit=2)[1])

    search_items = sorted(search_items, key=get_scp_number)

    if len(search_items) == 0:
        await message.reply(bold(_("errors.not_found")), "HTML")
        return

    page = await aioget(search_items[0]["url"])
    soup = BeautifulSoup(page.text, "lxml")

    content = soup.find_all("div", {"id": "page-content"})[0]
    images = content.find_all("img")

    parsed_text = (
        f"<b>{search_items[0]['title']}</b>\n\n" +
        TgHTML(str(content), ["div", {"class": "block-right"}]).parsed
    )

    if len(images) > 0:
        await message.answer_photo(
            images[0]["src"],
            cuteCrop(parsed_text, 1024),
            parse_mode="HTML"
        )

    else:
        await message.reply(cuteCrop(parsed_text, 4096), "HTML")
