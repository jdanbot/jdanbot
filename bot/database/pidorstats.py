from peewee import CharField, IntegerField, Model
from .connection import db


class PidorStats(Model):
    user_id = IntegerField()
    chat_id = IntegerField()
    username = CharField()
    count = IntegerField()

    class Meta:
        db_table = "pidor_stats"
        database = db
        primary_key = False
