from datetime import datetime

from .connection import db

from pytz import timezone
from peewee import IntegerField, DateTimeField, Model


TIMEZONE = timezone("Europe/Moscow")


class PidorEvent(Model):
    pidor_id = IntegerField()
    caused_at = DateTimeField(null=True, default=lambda: datetime.now(TIMEZONE))

    class Meta:
        db_table = "pidor_events"
        database = db
