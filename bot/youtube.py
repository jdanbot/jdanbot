from .bot import dp, bot
import urllib


async def get_video_id(url):
    try:
        return urllib.parse.parse_qs(urllib.parse.urlparse(url).query)["v"][0]
    except Exception:
        return url.replace('&feature=share', '').split('/')[-1]


@dp.message_handler(commands=["preview"])
async def preview(message):
    try:
        url = message.reply_to_message.text
    except AttributeError:
        url = message.text.split(maxsplit=1)[1]

    download_url = "https://img.youtube.com/vi/{id}/maxresdefault.jpg"
    video_id = await get_video_id(url)

    await bot.send_chat_action(message.chat.id, "upload_photo")
    await message.reply_photo(download_url.format(id=video_id))
