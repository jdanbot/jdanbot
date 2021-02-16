from ..config import dp
from ..lib.aioget import aioget

from bs4 import BeautifulSoup


@dp.message_handler(commands=["bashorg", "bashim", "b"])
async def bashorg(message):
    params = message.text.split(maxsplit=1)
    if len(params) == 1:
        page = await aioget("https://bash.im/random")
    else:
        try:
            num = int(params[1])
        except ValueError:
            await message.reply("Введи число")
            return

        page = await aioget(f"https://bash.im/quote/{num}")

    text = await page.text()

    soup = BeautifulSoup(text.replace("<br>", "\n"), 'lxml')
    soup2 = soup.find("div", class_="quote__body")

    for tag in soup2.find_all("div", {"class": "quote__strips"}):
        tag.replace_with("")

    soup2 = soup2.text \
                 .replace('<div class="quote__body">', "") \
                 .replace("</div>", "") \
                 .replace("<br\\>", "\n")

    await message.reply(soup2)
