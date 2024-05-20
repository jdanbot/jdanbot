from typing import Optional, TYPE_CHECKING

from aiogram import types
from piccolo.query.methods.select import Count
from sqlalchemy import func
from sqlmodel import Field, Relationship, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession


from . import tables as t
from .lib import unpack_needen, IdModel


if TYPE_CHECKING:
    from .member import Member


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: Optional[str] = Field(default=None)
    first_name: str
    last_name: Optional[str] = Field(default=None)

    user: list["Member"] = Relationship(
        # back_populates="user"
    )

    @property
    def full_name(self) -> str:
        if self.last_name:
            return " ".join([self.first_name, self.last_name])

        return self.first_name

    @property
    def mention(self) -> str:
        return self.user.username or self.user.full_name

    @staticmethod
    async def get_by(
        conn: AsyncSession, message: types.Message
    ) -> IdModel:
        return await conn.merge(
            User(
                **unpack_needen(
                    message.from_user,
                    {"id", "username", "first_name", "last_name"},
                ),
            )
        )

    async def get_pidor_count(self, conn: AsyncSession) -> int:
        return (
            await t.PidorEvent.select(
                Count(alias="count"),
            )
            .where(t.PidorEvent.pidor.user.id == self.id)
            .first()
        )["count"]

    @staticmethod
    async def count(conn: AsyncSession) -> int:
        res = await conn.exec(func.count(User.id))

        return res.first()[0]
