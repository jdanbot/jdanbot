from aiogram import types

from peewee import CharField, IntegerField, Model
from .connection import db


class Event(Model):
    chat_id = IntegerField()
    user_id = IntegerField()
    name = CharField()

    class Meta:
        db_table = "events"
        database = db
        primary_key = False

    def reg_user_in_db(message: types.Message) -> bool:
        # TODO: USE CREATE_OR_GET

        user = message.from_user
        cur_user = list(
            Event.select()
            .where(Event.user_id == user.id,
                   Event.chat_id == message.chat.id)
        )

        if len(cur_user) == 0:
            Event.insert(
                chat_id=message.chat.id,
                user_id=user.id,
                name=user.full_name
            ).execute()

            return True
        return False
