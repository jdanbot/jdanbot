import datetime

from .connection import db
from peewee import fn, SQL

from .pidor_event import PidorEvent

from peewee import IntegerField, BooleanField, ForeignKeyField, Model


class Pidor(Model):
    member_id = IntegerField()
    is_pidor_allowed = BooleanField(default=True)
    latest_pidor_event = ForeignKeyField(
        PidorEvent, column_name="latest_pidor_event", null=True)

    class Meta:
        db_table = "pidors"
        database = db

    @property
    def count(self) -> int:
        return (
            PidorEvent
                .select(fn.Count(SQL("*")))
                .where(PidorEvent.pidor_id == self.id)
        ).count()

    @property
    def when_pidor_of_day(self) -> datetime.datetime:
        return self.latest_pidor_event.caused_at
