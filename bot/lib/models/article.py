from dataclasses import dataclass
from typing import Optional

from aiogram import types

from ..text import cute_crop


@dataclass
class Article:
    text: str
    image: Optional[str] = None
    keyboard: Optional[types.InlineKeyboardMarkup] = None

    def __post_init__(self):
        limit = 1024 if self.image else 4096

        if (new_text := cute_crop(self.text, limit=limit)) != "":
            self.text = new_text
        else:
            self.text[:limit]
