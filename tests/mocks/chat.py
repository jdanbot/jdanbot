from aiogram import types
from pydantic import BaseModel


class ChatMock(BaseModel):
    id: int = -10020000000
    type: str = "supergroup"

    title: str = "jdan's secret test chat"
    username: str = "savekanobu"

    full_name = types.Chat.full_name

    async def restrict(self, *args, **kwargs):
        pass
