import json

from .connection import db

from peewee import CharField, Model


class Video(Model):
    channelid = CharField()
    link = CharField()

    class Meta:
        db_table = "videos"
        database = db
        primary_key = False

    def save(channelid, link):
        links = list(Video.select().where(Video.channelid == link))

        if len(links) > 0:
            links = json.loads(links[0].link)[-15:]
            links.append(link)

            links_str = json.dumps(links)

            (Video.update(link=links_str)
                  .where(Video.channelid == channelid)
                  .execute())

        else:
            links = [link]
            links_str = json.dumps(links)

            Video.insert(channelid=channelid, link=links_str).execute()
