from datetime import datetime, timedelta

from .connection import db
from ..config.bot import bot

from .chat_member import ChatMember
from .chat import Chat

from peewee import CharField, DateTimeField, ForeignKeyField, Model
from aiogram.utils import exceptions


class Poll(Model):
    author = ForeignKeyField(ChatMember, column_name="author_id")
    created_at = DateTimeField(default=datetime.now)
    description = CharField()

    class Meta:
        db_table = "polls"
        database = db

    async def close(self):
        return await bot.stop_poll(self.author.chat.id, self.id)

    async def close_old():
        period = datetime.now() - timedelta(hours=24)
        polls = Poll.select().where(Poll.created_at <= period).execute()

        for poll in polls:
            try:
                poll_res = await poll.close()

            except (exceptions.PollHasAlreadyBeenClosed,
                    exceptions.MessageWithPollNotFound):
                (Poll.delete()
                     .where(Poll.created_at <= period,
                            Poll.id == poll.id).execute())

                continue

            if poll_res.is_closed:
                Poll.delete().where(Poll.created_at <= period).execute()

            else:
                await bot.stop_poll(poll.chat_id, poll.id)
