from aiogram.types import InputMediaPhoto

import json
from .config import bot, vk_api, Feed, VK_FEEDS
from .lib.text import cuteCrop


async def vk_timer():
    # TODO: REWRITE: Add support of music

    for feed in VK_FEEDS:
        feed_id = feed["feed_id"]
        posts = await vk_api.wall.get(domain=feed_id, count=5, v="5.131")

        for item in posts["items"][::-1]:
            links = []
            feeds = list(Feed.select().where(Feed.id == feed_id))

            if len(feeds) == 0:
                Feed.save(feed_id, item["id"])
            else:
                if item["id"] in json.loads(feeds[0].links):
                    continue
                else:
                    Feed.save(feed_id, item["id"])

            try:
                attachments = item["attachments"]
            except Exception:
                attachments = []

            for attachment in attachments:
                if attachment["type"] == "photo":
                    url = get_max_photosize(attachment["photo"])
                    links.append(url)

                elif attachment["type"] == "video":
                    url = get_max_photosize(attachment["video"])
                    links.append(url)

            if len(links) == 1:
                await bot.send_photo(feed["chat_id"], links[0],
                                     cuteCrop(item["text"], 1000))

            elif len(links) > 1:
                photos = []

                for link in links:
                    photos.append(InputMediaPhoto(link))

                if item["text"] != "":
                    photos[0] = InputMediaPhoto(links[0],
                                                cuteCrop(item["text"], 1000))

                await bot.send_media_group(feed["chat_id"], photos)

            elif item["text"] != "":
                await bot.send_message(feed["chat_id"],
                                       cuteCrop(item["text"], 4096))


def get_max_photosize(photo, limit=130):
    sizes = []

    for key in photo.keys():
        if key.startswith("photo"):
            sizes.append(int(key[6:]))

    if max(sizes) >= limit:
        return photo[f"photo_{max(sizes)}"]
