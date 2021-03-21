from aiogram.types import InputMediaPhoto
from sqlfocus import SQLTable

import json
from .config import bot, conn, vk_api, VK_CHANNELS
from .lib.text import cuteCrop
from .timer import saveVideo


async def vk_timer():
    for channel in VK_CHANNELS:
        channelid = channel["channelid"]
        posts = await vk_api.wall.get(domain=channelid, count=5)

        for item in posts["items"][::-1]:
            links = []

            table = SQLTable("videos", conn)
            channels = await table.select(where=f"{channelid = }")

            if len(channels) == 0:
                await saveVideo(channelid, item["id"])
            else:
                if item["id"] in json.loads(channels[0][1]):
                    continue
                else:
                    await saveVideo(channelid, item["id"])

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
                await bot.send_photo(channel["chatid"], links[0],
                                     cuteCrop(item["text"], 1000))

            elif len(links) > 1:
                photos = []

                for link in links:
                    photos.append(InputMediaPhoto(link))

                if item["text"] != "":
                    photos[0] = InputMediaPhoto(links[0],
                                                cuteCrop(item["text"], 1000))

                await bot.send_media_group(channel["chatid"], photos)

            elif item["text"] != "":
                await bot.send_message(channel["chatid"],
                                       cuteCrop(item["text"], 4096))


def get_max_photosize(photo, limit=130):
    sizes = []

    for key in photo.keys():
        if key.startswith("photo"):
            sizes.append(int(key[6:]))

    if max(sizes) >= limit:
        return photo[f"photo_{max(sizes)}"]
