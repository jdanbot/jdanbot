import asyncio

from .config import conn, bot, DELAY, RSS_FEEDS
from .lib.aioget import aioget

import feedparser


async def timer():
    for feed in RSS_FEEDS:
        response = await aioget(feed["url"])
        cur = await conn.cursor()

        xml = feedparser.parse(await response.text())
        first_video = xml["entries"][0]["link"]

        sql = 'SELECT * FROM videos WHERE channelid="{id}"'
        channels = await cur.execute(sql.format(
            id=feed["channelid"]
        ))

        channels = await channels.fetchall()

        if len(channels) == 0:
            await bot.send_message(feed["chatid"], first_video)
            await saveVideo(feed["channelid"], first_video)
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

                await saveVideo(feed["channelid"], first_video)

        await conn.commit()


async def saveVideo(channelid, link):
    cur = await conn.cursor()

    await cur.execute('DELETE FROM videos WHERE channelid="{id}"'.format(
        id=channelid
    ))

    await cur.execute('INSERT INTO videos VALUES ("{id}", "{link}")'.format(
        id=channelid,
        link=link
    ))

    await conn.commit()


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(DELAY, repeat, coro, loop)
