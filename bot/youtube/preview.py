from aiogram import types
import urllib

from ..config import dp
from .. import handlers


max_url = "https://img.youtube.com/vi/{id}/maxresdefault.jpg"
hq_url = "https://img.youtube.com/vi/{id}/hqdefault.jpg"


def get_video_id(url: str) -> str:
    try:
        return urllib.parse.parse_qs(urllib.parse.urlparse(url).query)["v"][0]
    except Exception:
        return url.replace("&feature=share", "").split("/")[-1]


@dp.message_handler(commands=["preview"])
@handlers.get_text
async def preview(message: types.Message, url: str):
    video_id = get_video_id(url)
    await message.answer_chat_action("upload_photo")

    try:
        await message.reply_photo(
            max_url.format(id=video_id)
        )
    except Exception:
        await message.reply_photo(
            hq_url.format(id=video_id)
        )
