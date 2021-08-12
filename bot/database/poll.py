import datetime

from .connection import db, manager
from ..config.bot import bot

from peewee import *
from aiogram.utils import exceptions


class Poll(Model):
    user_id = IntegerField()
    chat_id = IntegerField()
    poll_id = IntegerField()
    timestamp = IntegerField()
    description = CharField()

    class Meta:
        db_table = "polls"
        database = db
        primary_key = False

    async def add(user_id, chat_id,
                  poll_id, description):
        now = datetime.datetime.now()
        period = int(now.timestamp())

        await manager.execute(
            Poll.insert(chat_id=chat_id, user_id=user_id,
                        poll_id=poll_id, description=description,
                        timestamp=period)
        )

    async def close_old():
        period = datetime.timedelta(hours=24)
        now = datetime.datetime.now()
        period_bound = int((now - period).timestamp())

        polls = await manager.execute(
            Poll.select()
                .where(Poll.timestamp <= period_bound)
        )

        for poll in polls:
            try:
                poll_res = await bot.stop_poll(poll.chat_id,
                                               poll.poll_id)

            except (exceptions.PollHasAlreadyBeenClosed,
                    exceptions.MessageWithPollNotFound):
                await manager.execute(
                    Poll.delete()
                        .where(Poll.timestamp <= period_bound,
                               Poll.chat_id == poll.chat_id,
                               Poll.poll_id == poll.poll_id)
                )

                continue

            if poll_res.is_closed:
                await manager.execute(
                    Poll.delete()
                        .where(Poll.timestamp <= period_bound)
                )

            else:
                await bot.stop_poll(poll.chat_id, poll.poll_id)