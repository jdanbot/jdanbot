from typing import Any

from aiogram import types
from aiogram.utils.markdown import hide_link
from pydantic import BaseModel
from selectolax.lexbor import LexborHTMLParser

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
                    self.bold2link(self.text).replace(
                        "&nbsp;", " "
                    ),
                ]
            )
        )

    def bold2link(self, text: str) -> str:
        if self.href is None:
            return text

        sel = LexborHTMLParser(text)

        html = sel.html or ""
        b = sel.css("b, strong")

        if html.startswith(self.title):
            return self.bold2link(
                f"<b>{self.title}</b>"
                + html.removeprefix(self.title)
            )

        if (
            len(b) == 0 or self.force_add_title
        ) and self.title:
            html = html.replace(" – ", " — ")
            self.force_add_title = False

            if (
                "Beholder" in html
                or html.split(" — ", maxsplit=1)[0]
                == self.title
            ):
                return self.bold2link(
                    html.replace(
                        f"{self.title} — ",
                        f"<b>{self.title}</b> — ",
                    )
                )
            else:
                return self.bold2link(
                    f"<b>{self.title}</b>\n\n{html}"
                )

        if len(b) > 0:
            b[0].replace_with(
                LexborHTMLParser(
                    f"""<b><a href="{self.href}">{b[0].inner_html}</a></b>"""
                ).body.child
            )
            return sel.body.inner_html

        return text
