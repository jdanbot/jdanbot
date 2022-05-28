from ...lib.aioget import aioget
from ...lib.models.article import Article

from dataclasses import dataclass

from bs4 import BeautifulSoup
from tghtml import TgHTML


@dataclass
class Result:
    title: str
    description: str
    url: str


class SCP:
    BASE_URL = "http://scp-ru.wikidot.com"

    async def search(self, query: str) -> list[Result]:
        r = await aioget(f"{self.BASE_URL}/search:site/q/{query}")

        soup = BeautifulSoup(r.text, "lxml")
        search_box = soup.find_all("div", class_="search-box")[0]

        return [Result(
            title=item.find("div", class_="title").a.text.strip(),
            description=item.find("div", class_="preview").text.strip(),
            url=item.find("div", class_="url").text.strip()
        ) for item in search_box.find_all("div", class_="item")]

    async def page(self, path: str, title: str = "") -> Article:
        r = await aioget(path if path.startswith(self.BASE_URL) else f"{self.BASE_URL}/{path}")

        soup = BeautifulSoup(r.text, "lxml")
        content = soup.find(id="page-content")

        if title == "":
            title = soup.find(id="page-title").text

        parsed_text = (
            f"<b>{title}</b>\n" +
            TgHTML(str(content), ["div", {"class": "block-right"}]).parsed
        )

        return Article(
            text=str(parsed_text),
            image=None if len(img := content.find_all("img")) == 0 else img[0]["src"]
        )
