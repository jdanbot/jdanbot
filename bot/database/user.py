from aiogram import types
from msgspec import convert
from pypika import PostgreSQLQuery as Query

from ..config.languages import Language
from ._base import Base, BetterConnection, dbmethod
from ._tables import U


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
        if (user := message.from_user) is None:
            raise KeyError

        user = await conn.execute_one(
            Query.into(U)  # type: ignore[operator]
            .columns(
                U.id, U.first_name, U.last_name, U.username
            )
            .insert(
                user.id,
                user.first_name,
                user.last_name,
                user.username,
            )
            .on_conflict(U.id)
            .do_update(U.first_name)
            .do_update(U.last_name)
            .do_update(U.username)
            .returning("*")
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
        user = await conn.execute_one(
            Query.from_(U).select("*").where(U.id == id)
        )

        if user is None:
            raise KeyError

        return convert(
            [*user, Language.from_str("ru")],
            User,
        )
