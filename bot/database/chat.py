from typing import Optional

from datetime import datetime, timedelta

from .connection import db
from .pidor import Pidor

from aiogram import types
from peewee import CharField, ForeignKeyField, Model


class Chat(Model):
    username = CharField()
    title = CharField()
    pidor = ForeignKeyField(Pidor, null=True, column_name="pidor_of_day_id")

    class Meta:
        db_table = "chats"
        database = db

    @property
    def all_pidors(self) -> list[Pidor]:
        from .chat_member import ChatMember

        return list(
            Pidor.select()
                 .join(ChatMember, on=ChatMember.pidor_id == Pidor.id)
                 .join(Chat, on=ChatMember.chat_id == Chat.id)
                 .where(Chat.id == self.id, Pidor.is_pidor_allowed == True)
        )

    @property
    def can_run_pidor_finder(self) -> bool:
        if self.pidor is None:
            return True
            
        period_bound = datetime.now() - timedelta(hours=24)
        return self.pidor.when_pidor_of_day <= period_bound

    def get_by_message(message: types.Message) -> "Chat":
        chat = message.chat
        defaults = dict(chat.title, username=chat.username)

        if chat.id > 0:
            chat.title = message.from_user.full_name

        Chat.get_or_create(id=chat.id, defaults=defaults)
        Chat.update(**defaults).where(Chat.id == chat.id).execute()

        return Chat.get_by_id(chat.id)
