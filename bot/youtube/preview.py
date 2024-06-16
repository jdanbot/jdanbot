from aiogram import types
from aiogram.filters import Command
from httpx import URL

from ..config import bot, router
from ..filters import GetText

max_url = "https://img.youtube.com/vi/{id}/maxresdefault.jpg"
hq_url = "https://img.youtube.com/vi/{id}/hqdefault.jpg"


def get_video_id(url: str) -> str:
    try:
        return URL(url).params["v"]
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
