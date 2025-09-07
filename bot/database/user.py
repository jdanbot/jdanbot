from aiogram import types
from tortoise import fields
from tortoise.fields import Field

from .lib.base_table import BaseTable
from .pidor import PidorEvent


class User(BaseTable):
    id: int | Field[int] = fields.BigIntField(pk=True, default=None)

    first_name: str | Field[str] = fields.TextField()
    last_name: str | None | Field[str] = fields.TextField(null=True)
    username: str | None | Field[str] = fields.TextField(null=True)

    # def __str__(self):
    #     return f"{self.id} {self.full_name}"

    @property
    def full_name(self) -> str:
        if self.last_name:
            return " ".join([self.first_name, self.last_name])

        return self.first_name

    @property
    def mention(self) -> str:
        return self.username or self.full_name

    @staticmethod
    async def get_by(message: types.Message) -> "User":
        return (
            await User.update_or_create(
                id=message.from_user.id,
                defaults=message.from_user.model_dump(
                    include={"username", "first_name", "last_name"}
                ),
            )
        )[0]

    def get_pidor_count(self) -> int:
        return PidorEvent.filter(pidor__user=self.id).count()
