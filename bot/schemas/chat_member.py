from datetime import datetime

from aiogram import types
from bot.lib.admin import check_admin
from peewee import BooleanField, DateTimeField, ForeignKeyField, Model

from ..config.bot import bot
from .chat import Chat
from .connection import db
from .pidor import Pidor
from .user import User


class ChatMember(Model):
    chat = ForeignKeyField(Chat, column_name="chat_id")
    user = ForeignKeyField(User, column_name="user_id")
    pidor = ForeignKeyField(Pidor, column_name="pidor_id", null=True)

    when_joined = DateTimeField(default=datetime.now, null=True)
    is_admin = BooleanField(null=True)

    class Meta:
        db_table = "chat_members"
        database = db

    @property
    def from_user(self) -> types.User:
        return self.user

    get_mention = types.User.get_mention
    mention = types.User.mention

    @property
    def tag(self) -> None:
        return types.User.get_mention()

    @staticmethod
    def get_by_message(message: types.Message) -> "ChatMember":
        return ChatMember.get_or_create(
            user_id=User.get_by_message(message).id,
            chat_id=Chat.get_by_message(message).id
        )[0]

    def get_or_create_pidor(self) -> tuple["Pidor", bool]:
        if self.pidor is None:
            self.pidor, is_created = Pidor.get_or_create(member_id=self.id)

            (
                ChatMember
                .update(pidor_id=self.pidor.id)
                .where(ChatMember.id == self.id)
                .execute()
            )
        else:
            is_created = False

        return self.pidor, is_created

    async def check_admin(self) -> bool:
        is_admin = await check_admin(bot, self.chat.id, self.user.id)

        (
            ChatMember
            .update(is_admin=is_admin)
            .where(ChatMember.id == self.id)
            .execute()
        )

        return is_admin
