from aiogram import types
import urllib

from aiogram.filters import Command
from ..config import router, bot
from ..filters import GetText

from aiogram.filters import Command


max_url = "https://img.youtube.com/vi/{id}/maxresdefault.jpg"
hq_url = "https://img.youtube.com/vi/{id}/hqdefault.jpg"


def get_video_id(url: str) -> str:
    try:
        return urllib.parse.parse_qs(
            urllib.parse.urlparse(url).query
        )["v"][0]
    except Exception:
        return url.replace("&feature=share", "").split("/")[-1]


@router.message(Command("preview"), GetText())
async def preview(message: types.Message, query: str):
    video_id = get_video_id(query)
    await bot.send_chat_action(message.chat.id, "upload_photo")

    try:
        await message.reply_photo(max_url.format(id=video_id))
    except Exception:
        await message.reply_photo(hq_url.format(id=video_id))
