from msgspec import convert
from whenever import Instant

from ._base import Base, BetterConnection, dbmethod, queries


class PidorEvent(Base, frozen=True):
    id: int
    pidor_id: int
    chat_id: int

    caused_at: Instant


class Pidor(Base, frozen=True):
    id: int
    chat_id: int
    user_id: int

    is_allowed: bool
    latest_time: int | None  # backed by latest_time_id

    @dbmethod
    @staticmethod
    async def get(
        id: int, conn: BetterConnection
    ) -> "Pidor":
        _ = await queries.pidor.get(conn, id=id)

        return convert(_, Pidor)

    @dbmethod
    async def get_latest_datetime(
        self, timezone: str, conn: BetterConnection
    ) -> Instant | None:
        if self.latest_time is None:
            return None

        time = await queries.pidor.get_latest_datetime(
            conn, event_id=self.latest_time
        )

        return Instant.from_timestamp(time)

    @dbmethod
    async def get_pidor_count(
        self, conn: BetterConnection
    ) -> int:
        return await queries.pidor.get_pidor_count(
            conn, pidor_id=self.id
        )


class PidorInTop(Base, frozen=True):
    count: int

    first_name: str
    last_name: str | None
    username: str | None

    @property
    def full_name(self) -> str:
        if self.last_name:
            return " ".join(
                [self.first_name, self.last_name]
            )

        return self.first_name


type PidorTop = list[PidorInTop]
