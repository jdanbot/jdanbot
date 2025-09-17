from typing import Any

from aiogram import types
from aiogram.utils.markdown import hide_link
from bs4 import BeautifulSoup
from pydantic import BaseModel

from ..text import cute_crop


class Article(BaseModel):
    text: str
    format_schema: str = "{}"
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
        if self.force_format:
            self.text = "\n\n".join(
                list(
                    filter(
                        lambda x: x.strip() != "",
                        self.text.splitlines(),
                    )
                )
            )

        if (
            new_text := cute_crop(self.text, limit=4096)
        ) != "":
            self.text = new_text
        else:
            self.text[:4096]

    def get_text(self) -> str:
        return self.format_schema.format(
            "".join(
                [
                    hide_link(self.image)
                    if self.image
                    else "",
                    self.bold2link(self.text),
                ]
            )
        )

    def bold2link(self, text: str) -> str:
        if self.href is None:
            return text

        soup = BeautifulSoup(text, "html.parser")
        b = soup.find_all(["b", "strong"])

        if str(soup).startswith(self.title):
            return self.bold2link(
                f"<b>{self.title}</b>"
                + str(soup).removeprefix(self.title)
            )

        if (
            len(b) == 0 or self.force_add_title
        ) and self.title:
            soup = str(soup).replace(" – ", " — ")
            self.force_add_title = False

            if (
                "Beholder" in soup
                or soup.split(" — ", maxsplit=1)[0]
                == self.title
            ):
                return self.bold2link(
                    soup.replace(
                        f"{self.title} — ",
                        f"<b>{self.title}</b> — ",
                    )
                )
            else:
                return self.bold2link(
                    f"<b>{self.title}</b>\n\n{soup}"
                )

        if len(b) > 0:
            b = b[0]
            b.name = "a"
            b["href"] = self.href
            b = b.wrap(soup.new_tag("b"))

            return str(soup)

        return text
