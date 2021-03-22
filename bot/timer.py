from sqlfocus import SQLTable

import asyncio
import json

from logging import debug

from .config import conn, bot, RSS_FEEDS
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

    table = SQLTable("videos", conn)

    channels = await table.select(where=f"{channelid = }")

    if len(channels) == 0:
        await bot.send_message(chatid, first_video)
        await saveVideo(channelid, first_video)
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

            await saveVideo(channelid, first_video)

    await conn.commit()


async def rss_timer():
    for feed in RSS_FEEDS:
        await rss_task(feed["url"], feed["channelid"], feed["chatid"])


async def saveVideo(channelid, link):
    table = SQLTable("videos", conn)
    table.quote = "'"

    links = await table.select(where=f"{channelid = }")

    try:
        links = json.loads(links[0][1])[:9]
        links.append(link)
    except IndexError:
        links = [link]

    links_str = json.dumps(links)

    await table.delete(where=f"{channelid = }")
    await table.insert(channelid, links_str)

    await conn.commit()
