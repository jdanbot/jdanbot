from datetime import datetime, timedelta


class Warn: ...


# class Warn(BaseTable):
#     id: Field[int] | int = fields.IntField(pk=True)

#     who_warned_id: Field[int] | int = fields.IntField()

#     who_warn_id: Field[int] | int = fields.IntField()

#     reason: Field[str] | str | None = fields.TextField(
#         nullable=True
#     )
#     warned_at: Field[pdl.DateTime] | pdl.DateTime = (
#         fields.DatetimeField(auto_now=True)
#     )

#     @override
#     def __repr__(self) -> str:
#         return f"<Warn [{self.id}] m{self.who_warned_id} by m{self.who_warn_id}>"


class WarnOld:
    who_warned: int

    who_warn: int
    reason: str
    warned_at: datetime

    who_unwarn: int | None = None
    unwarn_reason: int | None = None
    unwarned_at: int | None = None

    @classmethod
    async def get_user_warns(
        cls,
        warned_id: int,
        period: timedelta = timedelta(hours=24),
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
