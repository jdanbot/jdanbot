import datetime

from peewee import *

from .connection import db, manager, get_count


class Warn(Model):
    admin_id = IntegerField()
    user_id = IntegerField()
    chat_id = IntegerField()
    timestamp = IntegerField()
    reason = CharField()

    class Meta:
        db_table = "warns"
        database = db
        primary_key = False

    async def count_wtbans(user_id, chat_id,
                           period=datetime.timedelta(hours=24)):
        period_bound = int((datetime.datetime.now() - period).timestamp())

        return get_count(await manager.execute(
            Warn.select(fn.Count(SQL("*")))
                .where(
                    Warn.timestamp >= period_bound,
                    Warn.user_id == user_id,
                    Warn.chat_id == chat_id
                )
        ))

    async def mark_chat_member(user_id, chat_id, admin_id, reason):
        await manager.execute(
            Warn.insert(user_id=user_id, admin_id=admin_id,
                        chat_id=chat_id, reason=reason,
                        timestamp=int(datetime.datetime.now().timestamp()))
        )