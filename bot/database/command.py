from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime

from . import tables as t


class Command(BaseModel):
    chat_id: int
    user_id: int

    name: str
    args: Optional[str] = None

    runned_at: datetime = Field(default_factory=datetime.now)

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
