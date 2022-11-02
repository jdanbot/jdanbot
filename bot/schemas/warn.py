from datetime import datetime, timedelta

from peewee import CharField, DateTimeField, IntegerField, Model
from .connection import db

from pytz import timezone


TIMEZONE = timezone("Europe/Moscow")


class Warn(Model):
    who_warned_id = IntegerField()

    who_warn_id = IntegerField()
    reason = CharField()
    warned_at = DateTimeField(default=lambda: datetime.now(TIMEZONE))

    who_unwarn_id = IntegerField(null=True)
    unwarn_reason = CharField(null=True)
    unwarned_at = DateTimeField(null=True)

    class Meta:
        db_table = "warns"
        database = db

    @staticmethod
    def get_user_warns(
        warned_id: int,
        period: timedelta = timedelta(hours=24)
    ) -> list["Warn"]:
        return Warn.get_warns(warned_id, period=period)

    @staticmethod
    def get_bound(period: timedelta) -> datetime:
        return datetime.now(TIMEZONE) - period

    @staticmethod
    def get_warns(
        warned_id: int | None = None,
        admin_id: int | None = None,
        period: timedelta | None = timedelta(hours=24),
        ignore_unwarned: bool = True
    ) -> list["Warn"]:
        params = []

        if isinstance(warned_id, int):
            params.append(Warn.who_warned_id == warned_id)
        elif isinstance(admin_id, int):
            params.append(Warn.who_warn_id == admin_id)
        else:
            raise AttributeError

        if period:
            params.append(Warn.warned_at >= Warn.get_bound(period))

        if ignore_unwarned:
            params.append(Warn.who_unwarn_id >> None)

        return Warn.select().where(*params)

    def unwarn_by(self, admin) -> bool:
        if self.who_unwarn_id != None:
            raise AttributeError()

        self.who_unwarn_id = admin.id
        self.unwarned_at = datetime.now(TIMEZONE)

        self.save()
