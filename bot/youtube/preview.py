from aiogram import types
import urllib

from ..config import router, bot
from .. import handlers

from aiogram.filters import Command, CommandObject
from fluentogram import FluentTranslator


max_url = "https://img.youtube.com/vi/{id}/maxresdefault.jpg"
hq_url = "https://img.youtube.com/vi/{id}/hqdefault.jpg"


def get_video_id(url: str) -> str:
    try:
        return urllib.parse.parse_qs(
            urllib.parse.urlparse(url).query
        )["v"][0]
    except Exception:
        return url.replace("&feature=share", "").split("/")[-1]


@router.message(Command("preview"))
@handlers.get_text
async def preview(
    message: types.Message,
    url: str,
    _: FluentTranslator,
    command: CommandObject,
):
    video_id = get_video_id(url)
    await bot.send_chat_action(message.chat.id, "upload_photo")

    try:
        await message.reply_photo(max_url.format(id=video_id))
    except Exception:
        await message.reply_photo(hq_url.format(id=video_id))
