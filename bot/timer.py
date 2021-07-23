import asyncio
import json

from logging import debug

from .config import bot, RSS_FEEDS, Video, YOUTUBE_KEY, manager
from .lib.aioget import aioget

import feedparser


async def youtube_task(channelid, chatid):
    url = "https://www.googleapis.com/youtube/v3/search"
    response = await aioget(url, timeout=5, params={
        "key": YOUTUBE_KEY,
        "channelId": channelid,
        "part": "id",
        "order": "date",
        "maxResults": 1
    })

    try:
        video = response.json()
    except asyncio.exceptions.TimeoutError:
        debug(f"[{channelid}] TimeoutError")
        return

    if video.get("error") is not None:
        return

    first_video = "https://www.youtube.com/watch?v={video_id}".format(
        video_id=video["items"][0]["id"]["videoId"]
    )

    await save_post(str(channelid), channelid, chatid, first_video)



async def rss_task(url, channelid, chatid):
    response = await aioget(url, timeout=5)

    xml = feedparser.parse(response.text)

    page = xml["entries"][0]
    first_url = page["link"]

    await save_post(url, channelid, chatid, first_url)


async def save_post(url, channelid, chatid, first_video):
    channels = list(await manager.execute(
        Video.select()
             .where(Video.channelid == channelid)
    ))

    if len(channels) == 0:
        await bot.send_message(chatid, first_video)
        await Video.save(channelid, first_video)
    else:
        if first_video in json.loads(channels[0].link):
            pass
        else:
            message = await bot.send_message(chatid, first_video)
            await bot.pin_chat_message(
                chatid,
                message.message_id,
                disable_notification=True
            )

            await Video.save(channelid, first_video)
