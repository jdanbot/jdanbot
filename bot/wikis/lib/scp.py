from dataclasses import dataclass

from bs4 import BeautifulSoup

from ...config.lib.tghtml import TgHTML
from ...lib.aioget import aioget
from ...lib.models.article import Article


@dataclass
class Result:
    title: str
    description: str
    url: str


class SCP:
    BASE_URL = "https://scpfoundation.net"

    @staticmethod
    async def page(path: str, title: str = "") -> Article:
        url = (
            path
            if path.startswith(SCP.BASE_URL)
            else f"{SCP.BASE_URL}/{path}"
        )
        r, text = await aioget(url)

        soup = BeautifulSoup(text, "lxml")
        content = soup.find(id="page-content")

        title = soup.find("title").text

        for tag in content.find_all(
            "div", class_="scp-image-caption"
        ):
            tag.p.replace_with("")

        for tag in content.find_all(
            "div", class_="collapsible-block"
        ):
            tag.replace_with("")

        img = content.find_all("img")

        for tag in content.find_all("div", class_="rimg"):
            tag.replace_with("")

        for tag in content.find_all(
            "div", class_="w-stars-rate-module"
        ):
            tag.replace_with("")

        if title == "":
            title = soup.find(id="page-title").text.strip()

        parsed_text = (
            f"<b>{title}</b>\n\n"
            + TgHTML(str(content)).parsed
        )

        return Article(
            text=parsed_text,
            title=title,
            image=(
                None
                if len(img) == 0
                else f"https:{url}"
                if (url := img[0]["src"]).startswith("//")
                else url
            ),
            href=r.url.__str__(),
        )
