from typing import Annotated, Optional

from async_property import async_property

from pydantic_extra_types.pendulum_dt import DateTime

from beanie import Document, Indexed
import pendulum as pdl


class PidorEvent(Document):
    chat_id: int
    caused_at: DateTime


class PidorEvents(Document):
    pidor_id: int
    events: list[PidorEvent] = []


class Pidor(Document):
    member_id: int
    is_allowed: bool = True
    _count: Annotated[int, Indexed(int)]
    pidor_events: PidorEvents
    latest_time: PidorEvent = None

    @async_property
    async def latest_time(self) -> DateTime:
        return False or (False).caused_at