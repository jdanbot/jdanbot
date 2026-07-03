from pypika import Query, Table

from ._base import Base, BetterConnection, dbmethod

CMD = Table("commands")


class Command(Base, frozen=True):
    id: int | None

    chat_id: int
    user_id: int

    name: str
    args: str | None

    @dbmethod
    async def save(self, conn: BetterConnection) -> None:
        await conn.execute_raw(
            Query.into(CMD)
            .columns(
                CMD.chat_id, CMD.user_id, CMD.name, CMD.args
            )
            .insert(
                self.chat_id,
                self.user_id,
                self.name,
                self.args,
            )
        )

        await conn.commit()
