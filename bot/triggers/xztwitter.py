from ..config import dp
from aiogram import types
from .. import handlers
import urllib.parse


@dp.message_handler(lambda x: "https://twitter.com/" in x.text.lower())
@handlers.check("enable_twitter_redirect")
async def replace_twitter(message: types.Message, **kwargs):
    for entitie in message.entities:
        raw_url = message.text[entitie.offset:entitie.offset + entitie.length]

        if entitie.type == "url" and raw_url.lower().startswith("https://twitter.com/"):
            url = urllib.parse.urlparse(raw_url)

            return await message.reply(
                url._replace(netloc="zxtwitter.com").geturl())
