from aiogram.types import InputMediaPhoto

import json
from ..config import bot, vk_api, VK_FEEDS
from ..schemas import Feed
from ..lib.text import cute_crop


async def vk_timer():
    # TODO: REWRITE: Add support of music

    for feed in VK_FEEDS:
        feed_id = feed["feed_id"]
        posts = await vk_api.wall.get(feed_id)

        for post in posts[::-1]:
            links = []
            feeds = list(Feed.select().where(Feed.id == feed_id))

            if len(feeds) == 0:
                Feed.save(feed_id, post.id)
            else:
                if post.id in json.loads(feeds[0].links):
                    continue
                else:
                    Feed.save(feed_id, post.id)

            try:
                attachments = post.attachments
            except Exception:
                attachments = []

            for attachment in attachments:
                media = attachment.__dict__.get(attachment.type)

                if media is not None and media.__dict__.get("sizes", None) is not None:
                    links.append(media.sizes[-1].url)

            if len(links) == 1:
                await bot.send_photo(feed["chat_id"], links[0],
                                     cute_crop(post.text, 1000))

            elif len(links) > 1:
                photos = []

                for link in links:
                    photos.append(InputMediaPhoto(link))

                if post.text != "":
                    photos[0] = InputMediaPhoto(links[0],
                                                cute_crop(post.text, 1000))

                await bot.send_media_group(feed["chat_id"], photos)

            elif post.text != "":
                await bot.send_message(feed["chat_id"],
                                       cute_crop(post.text, 4096))
