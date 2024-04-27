from typing import Annotated, Optional

from async_property import async_property

from pydantic_extra_types.pendulum_dt import DateTime

from aiogram import types

from pydantic import BaseModel
from beanie import Document, Indexed, Link
from beanie.operators import Push
from .patches import BetterDocument
from ..config import settings
import httpx
import orjson


class PidorEvent(BaseModel):
    chat_id: int
    pidor: Link["Pidor"]
    caused_at: DateTime


class PidorEvents(BaseModel):
    # pidor: Link["Pidor"]
    events: list[PidorEvent] = []


class Pidor(BaseModel):
    # member: Link["Member"]
    is_allowed: bool = True
    _count: Annotated[int, Indexed(int)]
    # pidor_events: PidorEvents
    latest_time: PidorEvent = None

    @async_property
    async def latest_time(self) -> DateTime:
        return False or (False).caused_at


class Chat(BaseModel):
    id: int
    username: Optional[str] = None
    title: Optional[str] = None

    members: list["Member"] = []

    @classmethod
    async def get_by(cls, message: types.Message) -> "Chat":
        chat = message.chat

        async with httpx.AsyncClient(base_url=settings.api_url) as client:
            res = await client.post(
                f"/chat/get/{chat.id}",
                data=orjson.dumps(dict(username=chat.username, title=chat.title)),
            )

            return Chat.parse_raw(res.text)


class User(BaseModel):
    id: int
    username: Optional[str] = None
    first_name: str
    last_name: Optional[str] = None

    @property
    def full_name(self) -> str:
        if self.last_name:
            return " ".join([self.first_name, self.last_name])

        return self.first_name

    @classmethod
    async def get_by(cls, message: types.Message) -> "User":
        user = message.from_user

        async with httpx.AsyncClient(base_url=settings.api_url) as client:
            res = await client.post(
                f"/user/get/{user.id}",
                data=orjson.dumps(
                    dict(
                        username=user.username,
                        first_name=user.first_name,
                        last_name=user.last_name,
                    )
                ),
            )

            return User.parse_raw(res.text)


class Member(BaseModel):
    id: str
    chat: Link[Chat] = None
    user: Link[User] = None

    pidor: Optional[Pidor] = None
    warns: Optional[bool] = None

    is_admin: Optional[bool] = None

    @property
    def mention(self) -> str:
        return self.user.username or self.user.full_name

    @classmethod
    async def get_by(cls, message: types.Message) -> "Member":
        user, chat = message.from_user, message.chat

        async with httpx.AsyncClient(base_url=settings.api_url) as client:
            await User.get_by(message)
            await Chat.get_by(message)

            res = await client.post(f"/member/get/{user.id}@{chat.id}")

            return Member.parse_raw(res.text)

    async def get_pidor(self) -> tuple["Pidor", bool]:
        if self.pidor:
            return self.pidor, False

        print(self)

        self.pidor = {"_count": 200}

        return (await self.save()).pidor, True
