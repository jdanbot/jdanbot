import contextlib

from aiogram import types
from aiogram.filters import Command
from yarl import URL

from ..config import bot, router
from ..filters import GetText

YOUTUBE_URL = "https://img.youtube.com"

max_url = "{base_url}/vi/{id}/maxresdefault.jpg"
hq_url = "{base_url}/vi/{id}/hqdefault.jpg"


def get_video_id(url: str) -> str:
    with contextlib.suppress():
        return URL(url).query["v"]

    return url.replace("&feature=share", "").split("/")[-1]


@router.message(Command("preview"), GetText())
async def preview(message: types.Message, query: str):
    video_id = get_video_id(query)

    await bot.send_chat_action(
        message.chat.id, "upload_photo"
    )

    try:
        await message.reply_photo(
            max_url.format(
                base_url=YOUTUBE_URL,
                id=video_id,
            )
        )
    except Exception:
        await message.reply_photo(
            hq_url.format(
                base_url=YOUTUBE_URL,
                id=video_id,
            )
        )
