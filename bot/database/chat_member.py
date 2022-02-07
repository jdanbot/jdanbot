from ..config.bot import bot
from .connection import db

from .chat import Chat
from .user import User
from .pidor import Pidor

from aiogram import types
from datetime import datetime
from peewee import BooleanField, DateTimeField, ForeignKeyField, Model


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
    def tag(self) -> str:
        if self.user.username:
            return f"@{self.user.username}"

        return f"<a href='tg://user?id={self.user.id}'>{self.user.first_name}</a>"

    @property
    def mention(self) -> str:
        return self.user.username or self.user.first_name

    def get_by_message(message: types.Message) -> "ChatMember":
        return ChatMember.get_or_create(
            user_id=User.get_by_message(message).id,
            chat_id=Chat.get_by_message(message).id
        )[0]

    def get_or_create_pidor(self) -> Pidor | bool:
        if self.pidor is None:
            self.pidor, status = Pidor.get_or_create(member_id=self.id)
            ChatMember.update(pidor_id=self.pidor.id).where(ChatMember.id == self.id).execute()
        else:
            status = False

        return self.pidor, status

    async def check_admin(self) -> bool:
        user = await bot.get_chat_member(self.chat.id, self.user.id)
        is_admin = user.is_chat_admin()

        ChatMember.update(is_admin=is_admin).where(ChatMember.id == self.id).execute()
        return is_admin
