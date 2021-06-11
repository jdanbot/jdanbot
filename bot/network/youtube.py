import urllib

from ..config import bot, dp, MAX_URL, HQ_URL
from ..lib import handlers


def get_video_id(url):
    try:
        return urllib.parse.parse_qs(urllib.parse.urlparse(url).query)["v"][0]
    except Exception:
        return url.replace("&feature=share", "").split("/")[-1]


@dp.message_handler(commands=["preview"])
@handlers.get_text
async def preview(message, url):
    video_id = get_video_id(url)

    await bot.send_chat_action(message.chat.id, "upload_photo")

    try:
        await message.reply_photo(MAX_URL.format(id=video_id))
    except Exception:
        await message.reply_photo(HQ_URL.format(id=video_id))
