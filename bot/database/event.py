from peewee import CharField, IntegerField, Model
from .connection import db


class Event(Model):
    chatid = IntegerField()
    id = IntegerField()
    name = CharField()

    class Meta:
        db_table = "events"
        database = db
        primary_key = False

    def reg_user_in_db(message):
        # TODO: USE CREATE_OR_GET

        user = message.from_user
        cur_user = list(
            Event.select()
            .where(Event.id == user.id,
                   Event.chatid == message.chat.id)
        )

        if len(cur_user) == 0:
            Event.insert(
                chatid=message.chat.id,
                id=user.id,
                name=user.full_name
            ).execute()

            return True
