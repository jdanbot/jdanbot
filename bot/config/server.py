import asyncio
import feedparser
from aiohttp import web


async def feed_callback(request):
    xml = await request.text()
    feed = feedparser.parse(xml)
    for e in feed.entries:
        text = (f'channel: {e.yt_channelid}\n'
                f'video_url: {e.link}\n'
                f'title: {e.title}')
        print(text)
    return web.HTTPCreated()  # 201


def hub_challenge(request):
    return web.Response(text=request.query['hub.challenge'])


app = web.Application()
resource = app.router.add_resource('/callback/{channel_id}')
resource.add_route('GET', hub_challenge)
resource.add_route('POST', feed_callback)
