from datetime import datetime
from peewee import CharField, DateTimeField, IntegerField, Model
from .connection import db


class Command(Model):
    member_id = IntegerField()
    command = CharField()
    params = CharField()
    when_runned = DateTimeField(default=datetime.now)

    class Meta:
        db_table = "commands"
        database = db
        primary_key = False
