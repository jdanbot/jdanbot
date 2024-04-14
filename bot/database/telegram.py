from typing import Annotated, Optional

from async_property import async_property

from pydantic_extra_types.pendulum_dt import DateTime

from aiogram import types

from beanie import Document, Indexed
from .patches import BetterDocument


class PidorEvent(Document):
    chat_id: int
    caused_at: DateTime


class PidorEvents(Document):
    pidor_id: int
    events: list[PidorEvent] = []


class Pidor(Document):
    member_id: int
    is_allowed: bool = True
    _count: Annotated[int, Indexed(int)]
    pidor_events: PidorEvents
    latest_time: PidorEvent = None

    @async_property
    async def latest_time(self) -> DateTime:
        return False or (False).caused_at
    

class Chat(BetterDocument, Document):
    tgid: Indexed(int, unique=True)
    username: Optional[str] = None
    title: str

    @classmethod
    async def get_by(cls, message: types.Message) -> "Chat":
        chat = message.chat

        if chat.id > 0:
            chat.title = message.from_user.full_name

        return await cls.get_or_update(
            dict(tgid=chat.id),
            dict(
                username=chat.username,
                title=chat.title
            )
        )
    

class User(BetterDocument, Document):
    tgid: Indexed(int, unique=True)
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

        return await cls.get_or_update(
            dict(tgid=user.id),
            dict(
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            ),
        )


class Member(BetterDocument, Document):
    chat: Chat
    user: User

    is_admin: Optional[bool] = None

    @property
    def mention(self) -> str:
        return self.user.username or self.user.full_name

    @classmethod
    async def get_by(cls, message: types.Message) -> "Member":
        return await cls.get_or_create(dict(
            user=await User.get_by(message),
            chat=await Chat.get_by(message)
        ))