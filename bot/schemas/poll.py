from aiogram import types
from datetime import datetime, timedelta

from .connection import db
from .chat_member import ChatMember
from ..config.bot import bot

from peewee import CharField, DateTimeField, ForeignKeyField, Model


class Poll(Model):
    author = ForeignKeyField(ChatMember, column_name="author_id")
    created_at = DateTimeField(default=datetime.now)
    description = CharField()

    class Meta:
        db_table = "polls"
        database = db

    async def close(self) -> types.Poll:
        Poll.delete().where(Poll.id == self.id).execute()
        return await bot.stop_poll(self.author.chat.id, self.id)

    async def close_old(period: timedelta = timedelta(hours=24)):
        polls = Poll.select().where(Poll.created_at <= datetime.now() - period)

        for poll in polls:
            await poll.close()
