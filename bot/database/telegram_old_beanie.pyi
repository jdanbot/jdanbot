from typing import Annotated, Optional

from async_property import async_property

from pydantic_extra_types.pendulum_dt import DateTime

from aiogram import types
from aiogram.utils.markdown import link, hlink, escape_md

from pydantic import BaseModel
from typing import ClassVar
from beanie import Document, Indexed, Link
from beanie.operators import Push
from .patches import BetterDocument


import pendulum as pdl

from pydantic import Field


class PidorEvent(BaseModel):
    pidor: Link["Member"]
    # caused_at: DateTime = Field(default_factory=pdl.now)


class Pidor(BaseModel):
    # member: Link["Member"]
    is_allowed: bool = True
    count: Annotated[int, Indexed(int)]
    # pidor_events: PidorEvents
    latest_time: Optional[PidorEvent] = None

    # async def latest_time(self) -> DateTime:
    #     return False or (False).caused_at


class Chat(BetterDocument, Document):
    tg_id: Indexed(int, unique=True)
    username: Optional[str] = None
    title: Optional[str] = None

    pidor_events: list[PidorEvent]
    pidor: Optional[Link["Member"]] = None

    @classmethod
    async def get_by(cls, message: types.Message) -> "Chat":
        chat = message.chat

        if chat.id > 0:
            chat.title = message.from_user.full_name

        return await cls.get_or_update(
            dict(tg_id=chat.id),
            dict(username=chat.username, title=chat.title, pidor_events=[]),
        )

    async def pidors(self) -> list["Member"]:
        return await Member.find(
            {"_id": {"$regex": f"@{self.tg_id}$"}},
            {"pidor": {"$exists": True}},
            {"pidor.is_allowed": {"$not": {"$eq": False}}},
        ).to_list()


class User(BetterDocument, Document):
    tg_id: Indexed(int, unique=True)
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
            dict(tg_id=user.id),
            dict(
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
            ),
        )


class Member(BetterDocument, Document):
    id: str
    chat: Link[Chat]
    user: Link[User]

    pidor: Optional[Pidor] = None
    warns: Optional[bool] = None

    is_admin: Optional[bool] = None

    @property
    def parse_id(self) -> tuple[int, int]:
        return map(int, self.id.split("@"))

    @property
    def mention(self) -> str:
        return self.user.username or self.user.full_name

    @property
    def tag(self, use_html=False) -> str:
        if self.user.username:
            return escape_md(f"@{self.user.username}")

        return (hlink if use_html else link)(self.user.full_name, f"tg://user?id={self.user.id}")


    @classmethod
    async def get_by(cls, message: types.Message) -> "Member":
        return await cls.get_or_update(
            dict(_id=f"{message.from_id}@{message.chat.id}"),
            dict(
                user=await User.get_by(message),
                chat=await Chat.get_by(message),
            ),
        )

    async def get_pidor(self) -> tuple["Pidor", bool]:
        if self.pidor:
            return self.pidor, False

        print(self)

        self.pidor = Pidor(count=0)
        print(self)
        await self.save()

        return self.pidor, True
