from peewee import CharField, IntegerField, Model
from .connection import db


class Command(Model):
    chat_id = IntegerField()
    user_id = IntegerField()
    command = CharField()

    class Meta:
        db_table = "commands"
        database = db
        primary_key = False
