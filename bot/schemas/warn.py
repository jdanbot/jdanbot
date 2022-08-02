from datetime import datetime, timedelta

from peewee import CharField, DateTimeField, IntegerField, Model
from .connection import db

from pytz import timezone


class Warn(Model):
    who_warned_id = IntegerField()

    who_warn_id = IntegerField()
    reason = CharField()
    warned_at = DateTimeField(default=datetime.now)

    who_unwarn_id = IntegerField(null=True)
    unwarn_reason = CharField(null=True)
    unwarned_at = DateTimeField(null=True)

    class Meta:
        db_table = "warns"
        database = db

    def count_warns(
        warned_id: int,
        period: timedelta = timedelta(hours=24)
    ) -> int:
        return Warn.get_user_warns(warned_id, period).count()

    def get_user_warns(
        warned_id: int,
        period: timedelta = timedelta(hours=24)
    ) -> list["Warn"]:
        _timezone = timezone("Europe/Moscow")
        period_bound = datetime.now(_timezone) - period

        return (Warn.select()
                    .where(
                        Warn.warned_at >= period_bound,
                        Warn.who_warned_id == warned_id,
                        Warn.who_unwarn_id >> None
                    ))

    def mark_chat_member(warned_id: int, admin_id: int, reason: str):
        Warn.insert(
            who_warned_id=warned_id,
            who_warn_id=admin_id,
            reason=reason
        ).execute()
