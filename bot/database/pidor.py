import datetime
from datetime import datetime as DateTime
from typing import Annotated, Optional, TYPE_CHECKING

from pydantic import BaseModel


from . import tables as t


if TYPE_CHECKING:
    from .member import Member
    from .user import User
    from .chat import Chat  # noqa


class PidorEvent(BaseModel):
    pidor: Annotated[int, "Member"]
    chat: Annotated[int, "Chat"]
    caused_at: datetime.datetime

    @property
    def pdl_caused_at(self) -> DateTime:
        return pdl.instance(self.caused_at)

    @classmethod
    async def insert(cls, pidor, chat) -> int:
        return (
            await t.PidorEvent.insert(
                t.PidorEvent(pidor=pidor.id, chat=chat.id)
            )
        )[0]["id"]


class Pidor(BaseModel):
    member: Optional["Member"] | int = None
    is_allowed: bool
    count: int = 0
    # pidor_events: PidorEvents
    latest_time: Optional[PidorEvent | int] = None

    async def get_latest_datetime(self) -> DateTime | None:
        if self.latest_time is None:
            return None

        return PidorEvent.parse_obj(
            await t.PidorEvent.get(self.latest_time)
        ).pdl_caused_at

    @classmethod
    async def count(cls) -> int:
        return await t.Pidor.count()


class PidorInTop(BaseModel):
    id: int
    user: "User"


class PidorTop(BaseModel):
    count: int
    pidor: PidorInTop

    def from_list(pidors_top: dict) -> list["PidorTop"]:
        return [PidorTop.parse_obj(pidor) for pidor in pidors_top]
