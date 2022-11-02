from datetime import datetime, timedelta

from aiogram import types
from bot.lib.admin import check_admin
from peewee import BooleanField, DateTimeField, ForeignKeyField, Model

from aiogram.utils.markdown import link, hlink, escape_md

from ..config.bot import bot
from .chat import Chat
from .connection import db
from .pidor import Pidor
from .user import User
from .warn import Warn


# TODO USE PENDULUM


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

    @property
    def tag(self, use_html=False) -> str:
        if self.user.username:
            return escape_md(f"@{self.user.username}")

        return (hlink if use_html else link)(self.user.full_name, f"tg://user?id={self.user.id}")

    @property
    def mention(self) -> str:
        return self.user.username or self.user.full_name

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

    @property
    def __day_warns(self): return Warn.get_warns(self.id)
    @property
    def __all_warns(self): return Warn.get_warns(self.id, period=None)
    @property
    def __admin_warns(self): return Warn.get_warns(
        admin_id=self.id,
        period=None,
        ignore_unwarned=False
    )

    @property
    def warns(self) -> list[Warn]:
        return list(self.__day_warns)

    @property
    def warn_counter(self) -> int:
        return self.__day_warns.count()

    @property
    def all_warns(self) -> list[Warn]:
        return list(self.__all_warns)

    @property
    def all_warn_counter(self) -> int:
        return self.__all_warns.count()

    @property
    def admin_warn_counter(self) -> list[Warn]:
        return self.__admin_warns.count()

    def warn_by(
        self,
        admin: "ChatMember",
        reason: str
    ) -> Warn:
        return Warn.create(
            who_warned_id=self.id,
            who_warn_id=admin.id,
            reason=reason
        )
