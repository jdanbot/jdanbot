import aiosqlite
from msgspec import convert
from whenever import Instant, PlainDateTime

from ._base import Base, queries


class PidorEvent(Base):
    id: int
    pidor_id: int
    chat_id: int

    caused_at: Instant


# class PidorEvent:
#     id: int | Field[int] = fields.IntField(pk=True)
#     pidor_id: int
#     pidor: fields.ForeignKeyRelation["Pidor"] = (
#         fields.ForeignKeyField("models.Pidor", default=None)
#     )
#     chat_id: int | Field[int] = fields.IntField()
#     caused_at = PendulumField(auto_now=True)


# class Pidor:
#     id: int = fields.IntField(pk=True)
#     chat_id: int = fields.IntField()
#     user_id: int

#     user: "Usera" = fields.ForeignKeyField(
#         "models.Usera", default=None
#     )

#     is_allowed: bool = fields.BooleanField(default=True)
#     latest_time: int | None = fields.IntField(null=True)


class Pidor(Base):
    id: int
    chat_id: int
    user_id: int

    is_allowed: bool
    latest_time: int | None  # backed by latest_time_id

    async def get(id: int) -> "Pidor":
        async with aiosqlite.connect("tortoise.db") as conn:
            _ = await queries.pidor.get(conn, id=id)

            return convert(
                (
                    *_[:-2],
                    bool(_[-2]),
                    _[-1],
                ),
                Pidor,
            )

        raise NotImplementedError

    async def get_latest_datetime(
        self, timezone: str
    ) -> Instant | None:
        if self.latest_time is None:
            return None

        async with aiosqlite.connect("tortoise.db") as conn:
            time = await queries.pidor.get_latest_datetime(
                conn, event_id=self.latest_time
            )

            from datetime import datetime

            return PlainDateTime.from_py_datetime(
                datetime.fromisoformat(time)
            ).assume_utc()

    async def get_pidor_count(self) -> int:
        async with aiosqlite.connect("tortoise.db") as conn:
            return await queries.pidor.get_pidor_count(conn, pidor_id=self.id)


class PidorInTop(Base):
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
