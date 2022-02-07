import datetime

from .connection import db

from peewee import IntegerField, BooleanField, DateTimeField, Model


class Pidor(Model):
    member_id = IntegerField()
    pidor_count = IntegerField(default=0)
    is_pidor_allowed = BooleanField(default=True)
    when_pidor_of_day = DateTimeField(null=True)

    class Meta:
        db_table = "pidors"
        database = db
