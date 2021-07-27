from peewee import *
from .connection import db, manager


class Event(Model):
    chatid = IntegerField()
    id = IntegerField()
    name = CharField()

    class Meta:
        db_table = "events"
        database = db
        primary_key = False

    async def reg_user_in_db(message):
        user = message.from_user

        cur_user = list(await manager.execute(
            Event.select()
                 .where(Event.id == user.id,
                        Event.chatid == message.chat.id)
        ))

        if len(cur_user) == 0:
            await manager.execute(
                Event.insert(
                    chatid=message.chat.id,
                    id=user.id,
                    name=user.full_name
                )
            )