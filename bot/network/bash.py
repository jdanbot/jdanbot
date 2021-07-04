from bs4 import BeautifulSoup

from ..config import dp, _
from ..lib import handlers
from ..lib.aioget import aioget


@dp.message_handler(commands=["bashorg", "bashim", "b"])
@handlers.parse_arguments(2, without_params=True)
async def bashorg(message, params):
    if len(params) == 1:
        page = await aioget("https://bash.im/random")
    else:
        try:
            num = int(params[1])
        except ValueError:
            message.reply(_("errors.invalid_post_id"))
            return

        page = await aioget(f"https://bash.im/quote/{num}")

    text = page.text

    soup = BeautifulSoup(text, 'lxml')
    body = soup.find("div", class_="quote__body")

    for br in body.find_all("br"):
        br.replace_with("\n")

    for tag in body.find_all("div", {"class": "quote__strips"}):
        tag.replace_with("")

    body = body.div.text \
               .replace('<div class="quote__body">', "") \
               .replace("</div>", "")

    await message.reply(body)
