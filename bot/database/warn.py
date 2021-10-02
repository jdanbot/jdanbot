import datetime

from peewee import CharField, IntegerField, Model, fn, SQL
from .connection import db


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

    async def count_warns(user_id, chat_id,
                          period=datetime.timedelta(hours=24)):
        period_bound = int((datetime.datetime.now() - period).timestamp())

        return (Warn.select(fn.Count(SQL("*")))
                    .where(
                        Warn.timestamp >= period_bound,
                        Warn.user_id == user_id,
                        Warn.chat_id == chat_id
                    ).count())

    def mark_chat_member(user_id, chat_id, admin_id, reason):
        Warn.insert(user_id=user_id, admin_id=admin_id,
                    chat_id=chat_id, reason=reason,
                    timestamp=int(datetime.datetime.now().timestamp())) \
            .execute()
