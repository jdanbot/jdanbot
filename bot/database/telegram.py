import datetime
from typing import Annotated, Optional

from aiogram import types
from aiogram.utils.markdown import hlink, link
from piccolo.query import OrderByRaw
from piccolo.query.methods.select import Count
from pydantic import BaseModel
from datetime import datetime as DateTime

from bot.lib.admin import check_admin

from ..config.bot import bot
from . import tables as t

from ..chat_misc.models import ChatModules, ChatSettings


class PidorEvent(BaseModel):
    pidor: Annotated[int, "Member"]
    chat: Annotated[int, "Chat"]
    caused_at: datetime.datetime

    @property
    def pdl_caused_at(self) -> DateTime:
        return pdl.instance(self.caused_at)

    @classmethod
    async def insert(cls, pidor, chat) -> int:
        return (
            await t.PidorEvent.insert(
                t.PidorEvent(pidor=pidor.id, chat=chat.id)
            )
        )[0]["id"]


class Pidor(BaseModel):
    member: Optional["Member"] | int = None
    is_allowed: bool
    count: int = 0
    # pidor_events: PidorEvents
    latest_time: Optional[PidorEvent | int] = None

    async def get_latest_datetime(self) -> DateTime | None:
        if self.latest_time is None:
            return None

        return PidorEvent.parse_obj(
            await t.PidorEvent.get(self.latest_time)
        ).pdl_caused_at

    @classmethod
    async def count(cls) -> int:
        return await t.Pidor.count()


class PidorTop(BaseModel):
    class PidorInTop(BaseModel):
        id: int
        user: "User"

    count: int
    pidor: PidorInTop

    def from_list(pidors_top: dict) -> list["PidorTop"]:
        return [PidorTop.parse_obj(pidor) for pidor in pidors_top]


class Chat(BaseModel):
    id: int
    username: Optional[str] = None
    title: Optional[str] = None

    pidor: Optional["Member"] | int = None

    @classmethod
    async def get_by(cls, message: types.Message) -> "Chat":
        chat = message.chat

        if chat.title is None:
            chat.title = message.from_user.full_name

        return Chat.parse_obj(
            await t.Chat.get_or_update(
                chat.id,
                dict(username=chat.username, title=chat.title),
            )
        )

    async def get_random_pidor(self) -> "Member":
        return Member.parse_obj(
            await t.Member.select(
                t.Member.id,
                t.Member.pidor.all_columns(),
                t.Member.user.all_columns(),
                t.Member.chat.all_columns(),
            )
            .where(t.Member.chat == self.id)
            .where(
                t.Member.pidor._.is_allowed.eq(True),
            )
            .order_by(OrderByRaw("random()"))
            .first()
            .output(nested=True)
        )

    async def get_pidor_count(self) -> int:
        return await (
            t.Member.count()
            .where(t.Member.chat.id == self.id)
            .where(t.Member.pidor.is_not_null())
            .where(t.Member.pidor._.is_allowed.eq(True))
        )

    async def can_run_pidor(self) -> bool:
        if self.pidor is None:
            return True

        pidor = Pidor.parse_obj(
            await t.Pidor.select()
            .where(t.Pidor.id == self.pidor)
            .first()
        )

        date = await pidor.get_latest_datetime()

        if date is None:
            return True

        timezone = pdl.timezone("Europe/Moscow")

        next_pidor_day = date.replace(tzinfo=timezone).replace(
            hour=0, minute=0, second=0, microsecond=0
        ) + pdl.duration(days=1)

        return pdl.now() >= next_pidor_day

    async def get_top_pidors(self, limit: int = 10) -> list[PidorTop]:
        return PidorTop.from_list(
            await t.PidorEvent.select(
                Count(),
                t.PidorEvent.pidor.id,
                t.PidorEvent.pidor.user._.all_columns(),
            )
            .where(t.PidorEvent.chat.id == self.id)
            .group_by(t.PidorEvent.pidor)
            .order_by(OrderByRaw("count"), ascending=False)
            .limit(limit)
            .output(nested=True)
        )

    async def get_members_count(self) -> int:
        return await t.Member.count().where(t.Member.chat == self.id)

    async def get_commands_count(self) -> int:
        return await t.Command.count().where(
            t.Command.chat_id == self.id
        )

    async def get_settings(self) -> ChatSettings:
        from .note import Note

        return ChatSettings(
            reactions=dict(
                rules=dict(
                    text=(
                        note_text := await Note.get(
                            self.id, "__rules__"
                        )
                    ),
                    is_enabled=note_text is not None,
                ),
                delete_joines=True,
            ),
            warns_to_ban=await Note.get(
                self.id,
                "__warns_to_ban__",
                default=3,
                type=lambda x, default: x
                if (x := int(x)) in (3, 5, -1)
                else default,
            ),
            language=await Note.get(
                self.id,
                "__chat_lang__",
                default="ru",
                type=lambda x, default: x
                if x in ("ru", "en", "uk")
                else default,
            ),
        )

    async def get_modules(self) -> ChatModules:
        from .note import Note, str2bool

        bool_params = dict(default=True, type=str2bool)

        return ChatModules(
            is_admin_enabled=await Note.get(
                self.id, "__enable_admin__", **bool_params
            ),
            is_selfmute_enabled=await Note.get(
                self.id, "__enable_selfmute__", **bool_params
            ),
            is_poll_enabled=await Note.get(
                self.id, "enable_poll", **bool_params
            ),
            is_memes_enabled=await Note.get(
                self.id, "__enable_response__", **bool_params
            ),
            is_ban_enabled=await Note.get(
                self.id, "enable_ban_trigger", **bool_params
            ),
        )


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

        return User.parse_obj(
            await t.User.get_or_update(
                user.id,
                dict(
                    username=user.username,
                    first_name=user.first_name,
                    last_name=user.last_name,
                ),
            )
        )

    async def get_pidor_count(self) -> int:
        return (
            await t.PidorEvent.select(
                Count(alias="count"),
            )
            .where(t.PidorEvent.pidor.user.id == self.id)
            .first()
        )["count"]

    @classmethod
    async def count(cls) -> int:
        return await t.User.count()


class Member(BaseModel):
    id: int
    chat: Chat | int
    user: User | int

    pidor: Optional[Pidor | int] = None
    warns: Optional[bool] = None

    is_admin: Optional[bool] = None

    @property
    def mention(self) -> str:
        return self.user.username or self.user.full_name

    @property
    def from_user(self) -> types.User:
        return self.user

    @property
    def tag(self, use_html=False) -> str:
        if self.user.username:
            return f"@{self.user.username}"

        return (hlink if use_html else link)(
            self.user.full_name, f"tg://user?id={self.user.id}"
        )

    @property
    def mention(self) -> str:
        return self.user.username or self.user.full_name

    async def check_admin(self) -> bool:
        is_admin = await check_admin(bot, self.chat.id, self.user.id)

        await t.Member.update(is_admin=is_admin).where(
            t.Member.id == self.id
        )

        return is_admin

    @classmethod
    async def get_by(
        cls, message: types.Message, pidor: bool = False
    ) -> "Member":
        member = await t.Member.objects().get_or_create(
            (t.Member.user == (await User.get_by(message)).id)
            & (t.Member.chat == (await Chat.get_by(message)).id)
        )

        return await cls.get_by_id(member.id, pidor)

    @classmethod
    async def get_id_by(cls, message: types.Message) -> int:
        return (await cls.get_by(message)).id

    @classmethod
    async def get_by_id(
        cls, id: int, pidor: bool = False
    ) -> "Member":
        return Member.parse_obj(
            await t.Member.select(
                t.Member.id,
                t.Member.chat.all_columns(),
                t.Member.user.all_columns(),
                (
                    t.Member.pidor.all_columns()
                    if pidor
                    else t.Member.pidor
                ),
            )
            .where(t.Member.id == id)
            .first()
            .output(nested=True)
        )

    @classmethod
    async def count(cls) -> int:
        return await t.Member.count()

    async def get_pidor_count(self) -> int:
        return (
            await t.PidorEvent.select(
                Count(alias="count"),
            )
            .where(t.PidorEvent.pidor.id == self.id)
            .first()
        )["count"]

    async def get_pidor(self) -> tuple["Pidor", bool]:
        if self.pidor:
            return await t.Pidor.get(self.pidor), False

        pidor = await t.Pidor.objects().get_or_create(
            where=t.Pidor.member == self.id
        )

        await t.Member.update(pidor=pidor).where(
            t.Member.id == self.id
        )

        return pidor, True

    async def get_in_chats_count(self) -> int:
        return await t.Member.count().where(
            t.Member.user == self.user.id
        )
