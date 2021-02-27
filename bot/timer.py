import asyncio

from .config import conn, bot, DELAY, RSS_FEEDS
from .lib.aioget import aioget

import feedparser


async def timer():
    for feed in RSS_FEEDS:
        response = await aioget(feed["url"])
        cur = conn.cursor()

        xml = feedparser.parse(await response.text())
        first_video = xml["entries"][0]["link"]

        sql = 'SELECT * FROM videos WHERE channelid="{id}"'
        channels = cur.execute(sql.format(
            id=feed["channelid"]
        )).fetchall()

        if len(channels) == 0:
            await bot.send_message(feed["chatid"], first_video)
            saveVideo(feed["channelid"], first_video)
        else:
            if channels[0][1] == first_video:
                pass
            else:
                message = await bot.send_message(feed["chatid"], first_video)
                await bot.pin_chat_message(
                    feed["chatid"],
                    message.message_id,
                    disable_notification=True
                )

                saveVideo(feed["channelid"], first_video)

        conn.commit()


def saveVideo(channelid, link):
    cur = conn.cursor()

    cur.execute('DELETE FROM videos WHERE channelid="{id}"'.format(
        id=channelid
    ))

    cur.execute('INSERT INTO videos VALUES ("{id}", "{link}")'.format(
        id=channelid,
        link=link
    ))

    conn.commit()


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(DELAY, repeat, coro, loop)
