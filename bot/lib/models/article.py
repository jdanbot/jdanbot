from dataclasses import dataclass
from typing import Any, Optional

from aiogram import types

from ..text import cute_crop


@dataclass
class Article:
    text: str
    title: str = None
    image: str = None

    keyboard: types.InlineKeyboardMarkup = None
    parse_mode: str = "HTML"
    disable_web_page_preview: bool = False

    force_format: bool = False

    href: str = ""
    params: Any = None

    def __post_init__(self):
        if self.force_format:
            self.text = "\n\n".join(list(filter(lambda x: x.strip() != "", self.text.splitlines())))

        TG_MESSAGE_LIMIT = 4096

        if (new_text := cute_crop(self.text, limit=TG_MESSAGE_LIMIT)) != "":
            self.text = new_text
        else:
            self.text[:TG_MESSAGE_LIMIT]
