from typing import Optional


from sqlalchemy import func
from sqlmodel import Field, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
import arrow


class Command(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    chat_id: int
    user_id: int

    name: str
    args: Optional[str] = Field(default=None)

    runned_at: datetime = Field(default_factory=datetime.now)

    @property
    def _runned_at(self) -> arrow.Arrow:
        return arrow.get(self.runned_at)

    async def count(conn: AsyncSession) -> int:
        res = await conn.exec(func.count(Command.id))

        return res.first()[0]
