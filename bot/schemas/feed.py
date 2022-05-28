import json

from .connection import db

from peewee import CharField, Model


class Feed(Model):
    id = CharField()
    links = CharField()

    class Meta:
        db_table = "feeds"
        database = db
        primary_key = False

    def save(feed_id: str, link: str):
        # TODO: went bool

        feeds = list(Feed.select().where(Feed.id == feed_id))

        if len(feeds) > 0:
            links = json.loads(feeds[0].links)[-15:]
            links.append(link)

            links_str = json.dumps(links)

            (Feed.update(links=links_str)
                 .where(Feed.id == feed_id)
                 .execute())

        else:
            links = [link]
            links_str = json.dumps(links)

            Feed.insert(id=feed_id, links=links_str).execute()
