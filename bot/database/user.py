from .connection import db

from aiogram import types
from peewee import CharField, Model


class User(Model):
    username = CharField(null=True)
    first_name = CharField()
    last_name = CharField(null=True)

    class Meta:
        db_table = "users"
        database = db

    @property
    def full_name(self) -> str:
        if self.last_name:
            return " ".join([self.first_name, self.last_name])

        return self.first_name

    def get_by_message(message: types.Message) -> "User":
        user = message.from_user
        defaults = dict(username=user.username, first_name=user.first_name, last_name=user.last_name)
        
        User.get_or_create(
            id=user.id, defaults=defaults
        )[0]

        User.update(**defaults).where(User.id == user.id).execute()

        return User.get_by_id(user.id)
