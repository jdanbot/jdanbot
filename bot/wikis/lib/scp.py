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

    async def page(self, path: str, title: str = "") -> Article:
        url = path if path.startswith(self.BASE_URL) else f"{self.BASE_URL}/{path}"
        r = await aioget(url)

        soup = BeautifulSoup(r.text, "lxml")
        content = soup.find(id="page-content")

        for tag in content.find_all("div", class_="scp-image-caption"):
            tag.p.replace_with("")

        if title == "":
            title = soup.find(id="page-title").text.strip()

        parsed_text = f"<b>{title}</b>\n\n" + TgHTML(str(content)).parsed
        
        return Article(
            text=str(parsed_text),
            image=None if len(img := content.find_all("img")) == 0 else img[0]["src"],
            href=url
        )
