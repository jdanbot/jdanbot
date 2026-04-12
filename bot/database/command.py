import aiosqlite

from ._base import Base, queries


class Command(Base):
    id: int | None

    chat_id: int
    user_id: int

    name: str
    args: str | None

    async def save(self) -> None:
        async with aiosqlite.connect("tortoise.db") as conn:
            await queries.log_command(
                conn,
                chat_id=self.chat_id,
                user_id=self.user_id,
                name=self.name,
                args=self.args,
            )

            await conn.commit()
