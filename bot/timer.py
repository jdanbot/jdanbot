from sqlfocus import SQLTable

import asyncio
import json

from logging import debug

from .config import conn, bot, RSS_FEEDS, videos
from .lib.aioget import aioget

import feedparser


async def rss_task(url, channelid, chatid):
    response = await aioget(url, timeout=3)

    try:
        text = await response.text()
    except asyncio.exceptions.TimeoutError:
        debug(f"[{channelid}] TimeoutError")
        return

    xml = feedparser.parse(text)
    first_video = xml["entries"][0]["link"]

    channels = await videos.select(where=f"{channelid = }")

    if len(channels) == 0:
        await bot.send_message(chatid, first_video)
        await videos.save(channelid, first_video)
    else:
        if first_video in json.loads(channels[0][1]):
            pass
        else:
            message = await bot.send_message(chatid, first_video)
            await bot.pin_chat_message(
                chatid,
                message.message_id,
                disable_notification=True
            )

            await videos.save(channelid, first_video)

    await conn.commit()


async def rss_timer():
    for feed in RSS_FEEDS:
        await rss_task(feed["url"], feed["channelid"], feed["chatid"])
