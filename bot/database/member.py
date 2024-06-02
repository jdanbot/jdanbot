from typing import TYPE_CHECKING

from aiogram import types
from aiogram.utils.markdown import hlink, link
from tortoise import fields

from bot.lib.admin import check_admin

from ..config.bot import bot
from .chat import Chat
from .lib import BaseModel
from .note import Member_NoteExt
from .pidor import Pidor, PidorEvent
from .user import User
from .warn import Warn

if TYPE_CHECKING:
    from .pidor import Pidor


class Member(Member_NoteExt, BaseModel):
    id = fields.IntField(pk=True)
    is_admin = fields.BooleanField(null=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User"
    )
    chat: fields.ForeignKeyRelation[Chat] = fields.ForeignKeyField(
        "models.Chat"
    )

    pidor: fields.ForeignKeyRelation["Pidor"] = (
        fields.ForeignKeyField("models.Pidor", null=True)
    )

    user_id: int
    chat_id: int

    warns: fields.ReverseRelation
    warned: fields.ReverseRelation

    def __str__(self):
        return f"Member {self.user_id}@{self.chat_id}"

    @property
    def mention(self) -> str:
        return self.user.mention

    @property
    def tag(self, use_html=False) -> str:
        if self.user.username:
            return f"@{self.user.username}"

        return (hlink if use_html else link)(
            self.user.full_name, f"tg://user?id={self.user.id}"
        )

    async def check_admin(self) -> bool:
        self.is_admin = await check_admin(
            bot, self.chat_id, self.user_id
        )
        await self.save()

        return self.is_admin

    @staticmethod
    async def get_by(message: types.Message) -> "Member":
        return (
            await Member.get_or_create(
                chat=await Chat.get_by(message),
                user=await User.get_by(message),
            )
        )[0]

    @staticmethod
    async def get_by_id(id: int) -> "Member":
        return await Member.get(id=id)

    def get_members_count(self) -> int:
        return Member.filter(chat_id=self.chat.id).count()

    async def get_pidor_count(self) -> int:
        return await Member.filter(
            chat_id=self.chat_id, pidor__is_allowed=True
        ).count()

    async def get_status(self) -> str:
        return (
            await bot.get_chat_member(self.chat_id, self.user_id)
        ).status

    @staticmethod
    async def get_id_by(message: types.Message) -> int:
        return (await Member.get_by(message)).id

    async def get_pidor_events_count(self) -> int:
        return await PidorEvent.filter(pidor_id=self.id).count()

    async def get_pidor(self) -> tuple["Pidor", bool]:
        if self.pidor:
            return await Pidor.get(id=self.pidor_id), False

        pidor, _ = await Pidor.get_or_create(id=self.id)

        await self.update(pidor=pidor)
        return pidor, _

    def get_in_chats_count(self) -> int:
        return Member.filter(user_id=self.user.id).count()

    async def warn(self, victim: "Member", reason: str) -> Warn:
        return await Warn.create(
            who_warn_id=self.id,
            who_warned_id=victim.id,
            reason=reason,
        )
