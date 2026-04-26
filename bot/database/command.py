from ._base import Base, BetterConnection, dbmethod, queries


class Command(Base, frozen=True):
    id: int | None

    chat_id: int
    user_id: int

    name: str
    args: str | None

    @dbmethod
    async def save(self, conn: BetterConnection) -> None:
        await queries.log_command(
            conn,
            chat_id=self.chat_id,
            user_id=self.user_id,
            name=self.name,
            args=self.args,
        )

        await conn.commit()
