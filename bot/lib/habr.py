from bs4 import BeautifulSoup
from .aioget import aioget


class Habr:
    def __init__(self):
        self.url = "https://habr.com/ru/post/"

    async def page(self, id_):
        r = await aioget(f"{self.url}{id_}/")
        soup = BeautifulSoup(await r.text(), "lxml")

        page = f'<b>{soup.find("h1").span.text.upper()}</b>\n\n'
        page += soup.findAll("div", {"id": "post-content-body"})[0].text

        for tag in soup.findAll("div", {"id": "post-content-body"})[0] \
                       .findAll("h2"):
            page = page.replace(tag.text, f"\n<b>{tag.text}</b>")

        for tag in soup.findAll("div", {"id": "post-content-body"})[0] \
                       .findAll("h3"):
            page = page.replace(tag.text, f"\n<b>{tag.text}</b>")

        return page
