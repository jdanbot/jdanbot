from dataclasses import dataclass
from typing import Any, Optional

from aiogram import types

from ..text import cute_crop
from aiogram.utils.markdown import hide_link


from bs4 import BeautifulSoup


@dataclass
class Article:
    text: str
    title: str | None = None
    image: str | None = None
    href: str | None = None

    keyboard: types.InlineKeyboardMarkup | None = None
    parse_mode: str | None = "HTML"
    disable_web_page_preview: bool = False

    force_format: bool = False
    force_add_title: bool = False

    params: Any = None

    def __post_init__(self):
        if self.image == -1:
            self.image = None

        if self.force_format:
            self.text = "\n\n".join(
                list(filter(lambda x: x.strip() != "", self.text.splitlines()))
            )

        if (new_text := cute_crop(self.text, limit=4096)) != "":
            self.text = new_text
        else:
            self.text[:4096]

    def get_text(self) -> str:
        text = hide_link(self.image) if self.image else ""
        return text + self.bold2link(self.text, self.title)

    def bold2link(self, text: str | None, title: str | None = None) -> str:
        if self.href is None:
            return text

        soup = BeautifulSoup(text, "html.parser")
        b = soup.find_all(["b", "strong"])

        if ((len(b) == 0 or self.force_add_title)) and title:
            print(self.title)
            return self.bold2link(f"<b>{title}</b>\n\n{str(soup)}")

        if len(b) > 0:
            b = b[0]
            b.name = "a"
            b["href"] = self.href
            b = b.wrap(soup.new_tag("b"))

            return str(soup)

        return text
