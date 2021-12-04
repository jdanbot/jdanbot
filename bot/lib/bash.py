from dataclasses import dataclass

from ..config.lib.driver import HttpDriver
from .aioget import aioget

from bs4 import BeautifulSoup
from tghtml import TgHTML


@dataclass
class Quote:
    id: int
    time: str
    text: str

    @classmethod
    def parse(self, soup: BeautifulSoup) -> "Quote":
        for br in soup.find_all("br"):
            br.replace_with("\n")

        for tag in soup.find_all("div", {"class": "quote__strips"}):
            tag.replace_with("")

        return Quote(
            id=int(soup.header.a.text[1:]),
            time=soup.header.div.text.strip().replace("  ", " "),
            text=TgHTML(soup.find(class_="quote__body").text.strip()).parsed
        )


class BashOrg:
    BASE_URL = "https://bash.im"

    def __init__(self):
        self.driver = HttpDriver()

    async def get(self, path: str, params={}) -> str:
        return await aioget(self.BASE_URL + path)

    async def random(self) -> list[Quote]:
        r = await self.get("/random")
        soup = BeautifulSoup(r, features="lxml")

        quotes = soup.find_all("section", class_="quotes")[0] \
                     .find_all("div", class_="quote__frame")

        return [Quote.parse(quote) for quote in quotes]

    async def quote(self, id: int) -> Quote:
        r = await self.get(f"/quote/{id}")
        soup = BeautifulSoup(r, features="lxml")

        quote = soup.find_all("div", class_="quote__frame")[0]
        return Quote.parse(quote)
