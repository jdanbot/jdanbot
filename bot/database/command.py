from typing import Optional

from pydantic import BaseModel
from pydantic_extra_types.pendulum_dt import DateTime
import pendulum as pdl

from . import tables as t
from pydantic import Field


class Command(BaseModel):
    chat_id: int
    user_id: int

    name: str
    args: Optional[str] = str

    runned_at: DateTime = Field(default_factory=pdl.now)

    async def insert(self) -> "Command":
        return await t.Command.insert(
            t.Command(
                chat_id=self.chat_id,
                user_id=self.user_id,
                name=self.name,
                args=self.args,
            )
        )

    @classmethod
    async def count(cls) -> int:
        return await t.Command.count()