from datetime import datetime, timedelta

import pendulum as pdl
from typing import Optional, TYPE_CHECKING
from tortoise import fields
from .lib import BaseModel, PdlField


if TYPE_CHECKING:
    from .member import Member


class Warn(BaseModel):
    id: int = fields.IntField(pk=True)
    who_warned: fields.ForeignKeyRelation["Member"] = (
        fields.ForeignKeyField("models.Member", related_name="warns")
    )

    who_warn: fields.ForeignKeyRelation["Member"] = (
        fields.ForeignKeyField("models.Member", related_name="warned")
    )
    reason: str | None
    warned_at: pdl.DateTime = PdlField(auto_now=True)

    def __repr__(self) -> str:
        return f"<Warn [{self.id}] m{self.who_warned_id} by m{self.who_warn_id}>"


class WarnOld:
    who_warned: int

    who_warn: int
    reason: str
    warned_at: datetime

    who_unwarn: Optional[int] = None
    unwarn_reason: Optional[int] = None
    unwarned_at: Optional[int] = None

    @staticmethod
    async def count_warns(
        warned_id: int, period: timedelta = timedelta(hours=24)
    ) -> int:
        period_bound = datetime.now() - period

        return await (
            t.Warn.count()
            .where(t.Warn.warned_at >> period_bound)
            .where(t.Warn.who_warned == warned_id)
            .where(t.Warn.who_unwarn.is_null())
        )

    @classmethod
    async def get_user_warns(
        cls, warned_id: int, period: timedelta = timedelta(hours=24)
    ) -> list["Warn"]:
        period_bound = datetime.now() - period

        return await Warn.select().where(
            Warn.warned_at >= period_bound,
            Warn.who_warned_id == warned_id,
            Warn.who_unwarn_id >> None,
        )

    @classmethod
    async def mark_chat_member(
        cls, warned_id: int, admin_id: int, reason: str
    ):
        await cls.insert(
            who_warned=warned_id,
            who_warn=admin_id,
            reason=reason,
        )
