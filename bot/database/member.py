from typing import Optional, TYPE_CHECKING

from aiogram import types
from aiogram.utils.markdown import hlink, link
from piccolo.query.methods.select import Count
from sqlmodel import Field, Relationship, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from bot.lib.admin import check_admin

from sqlmodel import select
from sqlalchemy.orm import joinedload

from ..config.bot import bot
from . import tables as t

from .user import User
from .chat import Chat

if TYPE_CHECKING:
    from .pidor import Pidor


class Member(SQLModel, table=True):
    id: int = Field(primary_key=True)

    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="user")

    chat_id: int = Field(foreign_key="chat.id")
    chat: Chat = Relationship(back_populates="chat")

    # pidor: Optional[Pidor | int] = None
    # warns: Optional[bool] = None

    is_admin: Optional[bool] = None

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
        is_admin = await check_admin(bot, self.chat.id, self.user.id)

        await t.Member.update(is_admin=is_admin).where(
            t.Member.id == self.id
        )

        return is_admin

    @staticmethod
    async def get_by(
        conn: AsyncSession, message: types.Message
    ) -> "Member":
        user = await User.get_by(conn, message)
        chat = await Chat.get_by(conn, message)

        if res := await Member.get_raw_by(conn, message):
            return res

        await conn.merge(
            Member(user_id=user.id, chat_id=chat.id),
        )

        return await Member.get_raw_by(conn, message)

    @staticmethod
    async def get_raw_by(
        conn: AsyncSession, message: types.Message
    ) -> Optional["Member"]:
        raw = await conn.exec(
            select(Member)
            .options(
                joinedload(Member.user),
                joinedload(Member.chat),
            )
            .where(Member.chat_id == message.chat.id)
            .where(Member.user_id == message.from_user.id)
        )

        if res := raw.first():
            return res

    @classmethod
    async def get_id_by(cls, message: types.Message) -> int:
        return (await cls.get_by(message)).id

    @classmethod
    async def get_by_id(
        cls, id: int, pidor: bool = False
    ) -> "Member":
        return Member.parse_obj(
            await t.Member.select(
                t.Member.id,
                t.Member.chat.all_columns(),
                t.Member.user.all_columns(),
                (
                    t.Member.pidor.all_columns()
                    if pidor
                    else t.Member.pidor
                ),
            )
            .where(t.Member.id == id)
            .first()
            .output(nested=True)
        )

    @classmethod
    async def count(cls) -> int:
        return await t.Member.count()

    async def get_pidor_count(self) -> int:
        return (
            await t.PidorEvent.select(
                Count(alias="count"),
            )
            .where(t.PidorEvent.pidor.id == self.id)
            .first()
        )["count"]

    async def get_pidor(self) -> tuple["Pidor", bool]:
        if self.pidor:
            return await t.Pidor.get(self.pidor), False

        pidor = await t.Pidor.objects().get_or_create(
            where=t.Pidor.member == self.id
        )

        await t.Member.update(pidor=pidor).where(
            t.Member.id == self.id
        )

        return pidor, True

    async def get_in_chats_count(self) -> int:
        return await t.Member.count().where(
            t.Member.user == self.user.id
        )
