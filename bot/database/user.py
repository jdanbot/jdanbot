from typing import Optional

from aiogram import types
from tortoise import fields
from tortoise.fields import Field

from .lib import BaseModel
from .pidor import PidorEvent


class User(BaseModel):
    id: Field[int] = fields.BigIntField(pk=True)

    first_name: Field[str] = fields.TextField()
    last_name: Optional[Field[str]] = fields.TextField(null=True)
    username: Optional[Field[str]] = fields.TextField(null=True)

    def __str__(self):
        return f"{self.id} {self.full_name}"

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
