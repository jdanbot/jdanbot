import aiosqlite
from aiogram import types
from msgspec import convert

from ..config.languages import Language
from ._base import Base, queries, dbmethod, BetterConnection


class User(Base, frozen=True):
    id: int

    first_name: str
    last_name: str | None
    username: str | None

    language: Language | None

    @property
    def full_name(self) -> str:
        if self.last_name:
            return " ".join(
                [self.first_name, self.last_name]
            )

        return self.first_name

    @property
    def mention(self) -> str:
        return self.username or self.full_name

    @staticmethod
    @dbmethod
    async def get_by(
        message: types.Message,
        conn: BetterConnection,
    ) -> "User":
        if message.from_user is None:
            raise KeyError

        user = await queries.user.get_by(
            conn,
            **message.from_user.model_dump(
                include={
                    "username",
                    "first_name",
                    "last_name",
                    "id",
                }
            ),
        )
        await conn.commit()

        return convert(
            [*user, Language.from_str("ru")],
            User,
        )

    @staticmethod
    @dbmethod
    async def get(
        id: int, conn: BetterConnection
    ) -> "User":
        user = await queries.user.get(conn, id=id)

        return convert(
            [*user, Language.from_str("ru")],
            User,
        )
