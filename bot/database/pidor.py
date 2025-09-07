from typing import TYPE_CHECKING

import pendulum as pdl
from pydantic import BaseModel
from pydantic.type_adapter import TypeAdapter
from pydantic_extra_types.pendulum_dt import DateTime
from tortoise import fields
from tortoise.fields import Field

from .lib.base_table import BaseTable
from .lib.pdl_field import PendulumField

if TYPE_CHECKING:
    from .user import User


class PidorEvent(BaseTable):
    id: int | Field[int] = fields.IntField(pk=True)
    pidor_id: int
    pidor: fields.ForeignKeyRelation["Pidor"] = fields.ForeignKeyField(
        "models.Pidor", default=None
    )
    chat_id: int | Field[int] = fields.IntField()
    caused_at: DateTime | Field[pdl.DateTime] = PendulumField(auto_now=True)


class Pidor(BaseTable):
    id: int | Field[int] = fields.IntField(pk=True)
    chat_id: int | Field[int] = fields.IntField()
    user_id: int

    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", default=None
    )

    is_allowed: bool | Field[bool] = fields.BooleanField(default=True)
    latest_time: int | None | Field[int] = fields.IntField(null=True)

    async def get_latest_datetime(self) -> pdl.DateTime | None:
        if self.latest_time is None:
            return None

        print(f"{self.latest_time=}")

        event: PidorEvent = await PidorEvent.get(id=self.latest_time)

        return event.caused_at


class PidorInTop(BaseModel):
    count: int

    first_name: str
    last_name: str | None
    username: str | None

    @property
    def full_name(self) -> str:
        if self.last_name:
            return " ".join([self.first_name, self.last_name])

        return self.first_name


PidorTop: TypeAdapter[list[PidorInTop]] = TypeAdapter(list[PidorInTop])
