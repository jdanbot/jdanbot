import json

from .connection import db, manager

from peewee import *


class Video(Model):
    channelid = CharField()
    link = CharField()

    class Meta:
        db_table = "videos"
        database = db
        primary_key = False

    async def save(channelid, link):
        links = list(await manager.execute(
            Video.select()
                 .where(Video.channelid == channelid)
        ))

        if len(links) > 0:
            links = json.loads(links[0].link)[-15:]
            links.append(link)

            links_str = json.dumps(links)

            await manager.execute(
                Video.update(link=links_str)
                     .where(Video.channelid == channelid)
            )

        else:
            links = [link]
            links_str = json.dumps(links)

            await manager.execute(
                Video.insert(channelid=channelid,
                             link=links_str)
            )