from peewee import *
from .connection import db


class CommandStats(Model):
    chat_id = IntegerField()
    user_id = IntegerField()
    command = CharField()

    class Meta:
        db_table = "command_stats"
        database = db
        primary_key = False