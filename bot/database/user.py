import aiosqlite
from aiogram import types
from msgspec import convert

from ..config.languages import Language
from ._base import Base, queries


class User(Base):
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
    async def get_by(message: types.Message) -> "User":
        if message.from_user is None:
            raise KeyError

        async with aiosqlite.connect("tortoise.db") as conn:
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
    async def get(id: int) -> "User":
        async with aiosqlite.connect("tortoise.db") as conn:
            user = await queries.user.get(conn, id=id)

        # return convert(chat, Chat)
        return convert(
            [*user, Language.from_str("ru")],
            User,
        )
    async def update(*args, **kwargs):...
