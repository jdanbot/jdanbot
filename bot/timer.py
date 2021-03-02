import asyncio
import json

from logging import log, debug, info

from .config import conn, bot, DELAY, RSS_FEEDS
from .lib.aioget import aioget

import feedparser


async def rss_task():
    for feed in RSS_FEEDS:
        response = await aioget(feed["url"], timeout=3)

        try:
            text = await response.text()
        except asyncio.exceptions.TimeoutError:
            debug(f"[{feed['channelid']}] TimeoutError")
            return

        xml = feedparser.parse(text)
        first_video = xml["entries"][0]["link"]

        cur = await conn.cursor()

        sql = 'SELECT * FROM videos WHERE channelid="{id}"'
        channels = await cur.execute(sql.format(
            id=feed["channelid"]
        ))

        channels = await channels.fetchall()

        if len(channels) == 0:
            await bot.send_message(feed["chatid"], first_video)
            await saveVideo(feed["channelid"], first_video)
        else:
            if first_video in json.loads(channels[0][1]):
                pass
            else:
                message = await bot.send_message(feed["chatid"], first_video)
                await bot.pin_chat_message(
                    feed["chatid"],
                    message.message_id,
                    disable_notification=True
                )

                await saveVideo(feed["channelid"], first_video)

        await conn.commit()


async def saveVideo(channelid, link):
    cur = await conn.cursor()

    links = await cur.execute('SELECT * FROM videos WHERE channelid="{id}"'.format(
        id=channelid
    ))
    links = await links.fetchall()

    try:
        links = json.loads(links[0][1])
        links.append(link)
    except IndexError:
        links = [link]

    await cur.execute('DELETE FROM videos WHERE channelid="{id}"'.format(
        id=channelid
    ))

    await cur.execute("INSERT INTO videos VALUES ('{id}', '{link}')".format(
        id=channelid,
        link=json.dumps(links)
    ))

    await conn.commit()
