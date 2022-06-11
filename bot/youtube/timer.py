import asyncio
import json

from logging import debug

from ..config import bot
# from ..config import bot, YOUTUBE_KEY
from ..schemas import Feed
from ..lib.aioget import aioget

import feedparser


async def youtube_task(feed_id, chat_id):
    url = "https://www.googleapis.com/youtube/v3/search"
    response = await aioget(url, timeout=5, params={
        "key": YOUTUBE_KEY,
        "channelId": feed_id,
        "part": "id",
        "order": "date",
        "maxResults": 1
    })

    try:
        video = response.json()
    except asyncio.exceptions.TimeoutError:
        debug(f"[{feed_id}] TimeoutError")
        return

    if video.get("error") is not None:
        return

    first_video = "https://www.youtube.com/watch?v={video_id}".format(
        video_id=video["items"][0]["id"]["videoId"]
    )

    await save_post(str(feed_id), feed_id, chat_id, first_video)


async def rss_task(url, feed_id, chat_id):
    response = await aioget(url, timeout=5)

    xml = feedparser.parse(response.text)

    page = xml["entries"][0]
    first_url = page["link"]

    await save_post(url, feed_id, chat_id, first_url)


async def save_post(url, feed_id, chat_id, first_video):
    channels = list(Feed.select()
                        .where(Feed.id == feed_id))

    if len(channels) == 0:
        await bot.send_message(chat_id, first_video)
        Feed.save(feed_id, first_video)
    else:
        if first_video in json.loads(channels[0].links):
            return False

        message = await bot.send_message(chat_id, first_video)
        await bot.pin_chat_message(
            chat_id,
            message.message_id,
            disable_notification=True
        )

        Feed.save(feed_id, first_video)
