from typing import Optional, TYPE_CHECKING, List

from tortoise import fields
from tortoise.fields import Field

from pydantic import BaseModel as Model, TypeAdapter

from .lib import BaseModel, PdlField
import pendulum as pdl


if TYPE_CHECKING:
    from .member import Member
    from .chat import Chat


class PidorEvent(BaseModel):
    id: Field[int] = fields.IntField(pk=True)

    pidor: fields.ForeignKeyRelation["Member"] = (
        fields.ForeignKeyField("models.Member")
    )
    chat: fields.ForeignKeyRelation["Chat"] = fields.ForeignKeyField(
        "models.Chat"
    )
    caused_at: pdl.DateTime = PdlField(auto_now=True)


class Pidor(BaseModel):
    id: Field[int] = fields.BigIntField(pk=True)
    is_allowed: bool = fields.BooleanField(default=True)
    latest_time: Optional[int] = fields.IntField(null=True)

    async def get_latest_datetime(self) -> pdl.DateTime | None:
        if self.latest_time is None:
            return None

        print(f"{self.latest_time=}")

        event = await PidorEvent.get(id=self.latest_time)

        return event.caused_at


class PidorInTop(Model):
    count: int

    username: Optional[str]
    first_name: str
    last_name: Optional[str]

    @property
    def full_name(self) -> str:
        if self.last_name:
            return " ".join([self.first_name, self.last_name])

        return self.first_name


PidorTop = TypeAdapter(List[PidorInTop])
