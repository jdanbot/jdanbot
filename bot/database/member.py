from typing import Any, override

import aiosqlite
from aiogram import types
from aiogram.utils.markdown import hlink, link
from msgspec import Struct, convert
from whenever import Instant, Time

from bot.lib.admin import check_admin

from ..config.bot import bot
from ._base import queries
from .chat import Chat
from .pidor import Pidor_, PidorTop
from .user import User

# from .warn import Warn
# from .user import User


class PidorRepr(Struct, frozen=True):
    id: int
    latest_time: int | None


class Member(Struct, frozen=True):
    user_id: int
    chat_id: int

    first_name: str
    last_name: str | None
    username: str | None

    lang: str
    # user: types.User = Field(repr=False, default=None)
    chat: Chat
    pidor: Pidor_ | None = None

    def __rich_repr__(self):
        for field in self.__struct_fields__:
            if field == "pidor":
                pidor = getattr(self, field)
                yield (
                    "pidor",
                    PidorRepr(
                        id=pidor.id,
                        latest_time=pidor.latest_time,
                    )
                    if pidor is not None
                    else None,
                )
            elif field not in ["chat", "user"]:
                yield field, getattr(self, field)

    @override
    def __str__(self):
        return f"Member {self.user_id}@{self.chat_id}"

    @property
    def full_name(self) -> str:
        if self.last_name:
            return " ".join(
                [self.first_name, self.last_name]
            )

        return self.first_name

    @property
    def mention(self) -> str:
        return self.username or self.full_name

    @property
    def tag(self, use_html: bool = False) -> str:
        if self.username:
            return f"@{self.username}"

        return (hlink if use_html else link)(
            self.full_name,
            f"tg://user?id={self.user_id}",
        )

    @classmethod
    async def get_by(
        cls, message: types.Message
    ) -> "Member":
        chat: Chat = await Chat.get_by(message)
        user: User = await User.get_by(message)

        return convert(
            dict(
                user_id=user.id,
                chat_id=chat.id,
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                lang="ru",
                # user=message.from_user
                chat=chat,
            ),
            Member,
        )

    @classmethod
    async def get(
        cls,
        user_id: int,
        chat_id: int,
        pidor: Pidor_ | None = None,
    ) -> "Member":
        chat: Chat = await Chat.get(id=chat_id)
        user: User = await User.get(id=user_id)

        return convert(
            dict(
                user_id=user.id,
                chat_id=chat.id,
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                lang="ru",
                chat=chat,
                pidor=pidor,
            ),
            Member,
        )

    ############ NOTES ############

    @classmethod
    async def get_note(
        cls, name: str, default: Any = None
    ) -> Any:
        return None or default

    ############ PIDOR ############

    async def is_pidor(self) -> bool:
        async with aiosqlite.connect("tortoise.db") as conn:
            return await queries.pidor.check_is_pidor(
                conn,
                chat_id=self.chat_id,
                user_id=self.user_id,
            )

    async def get_pidor(self) -> tuple[Pidor_, bool]:
        async with aiosqlite.connect("tortoise.db") as conn:
            _ = await queries.pidor.get_or_create(
                conn,
                chat_id=self.chat_id,
                user_id=self.user_id,
            )
            await conn.commit()

        return (
            convert(
                (
                    *_[:-3],
                    bool(_[-3]),
                    _[-2],
                ),
                Pidor_,
            ),
            bool(_[-1]),
        )

    async def become_today_pidor(self):
        assert self.pidor is not None, "???"

        async with aiosqlite.connect("tortoise.db") as conn:
            event_id = await queries.pidor.new_pidor_event(
                conn,
                pidor_id=self.pidor.id,
                chat_id=self.chat.id,
            )
            await queries.pidor.update_latest_time(
                conn,
                pidor_id=self.pidor.id,
                event_id=event_id,
            )
            await queries.pidor.update_chat_pidor(
                conn,
                chat_id=self.chat.id,
                pidor_id=self.pidor.id,
            )

            await conn.commit()

    async def get_random_pidor(self) -> "Member":
        async with aiosqlite.connect("tortoise.db") as conn:
            _ = await queries.pidor.get_random_pidor(
                conn, chat_id=self.chat_id
            )

        if _ is None:
            raise KeyError

        pidor = convert(
            (
                *_[:-2],
                bool(_[-2]),
                _[-1],
            ),
            Pidor_,
        )

        return await Member.get(
            user_id=pidor.user_id,
            chat_id=pidor.chat_id,
            pidor=pidor,
        )

    async def get_status(self) -> str:
        return (
            await bot.get_chat_member(
                self.chat_id, self.user_id
            )
        ).status

    async def is_left(self) -> bool:
        return await self.get_status() == "left"

    async def get_pidor_count(self) -> int:
        async with aiosqlite.connect("tortoise.db") as conn:
            return (
                await queries.pidor.get_pidor_members_count(
                    conn, chat_id=self.chat_id
                )
            )

    async def get_top_pidors(
        self, limit: int = 10
    ) -> PidorTop:
        async with aiosqlite.connect("tortoise.db") as conn:
            _ = [
                i
                async for i in queries.pidor.get_top(
                    conn, chat_id=self.chat_id, limit=limit
                )
            ]

        return convert(_, PidorTop)

    async def check_run_pidor(self) -> bool:
        if self.chat.current_pidor_id is None:
            return True

        pidor: Pidor_ = await Pidor_.get(
            id=self.chat.current_pidor_id
        )

        timezone: str = "Europe/Moscow"
        date = await pidor.get_latest_datetime(timezone)

        if date is None:
            return True

        next_pidor_day = date.to_tz(timezone).replace_time(
            Time(
                hour=0,
                minute=0,
                second=0,
                nanosecond=0,
            )
        )

        return (
            Instant.now().to_tz(timezone) >= next_pidor_day
        )

    async def get_members_count(self) -> int:
        return -1

    async def get_in_chats_count(self) -> int:
        return -1
        return await Member.filter(
            user_id=self.user.id
        ).count()

    async def get_pidor_events_count(self) -> int:
        return -1

        pidor = await Pidor.get(
            user_id=self.user_id, chat_id=self.chat_id
        )
        return await PidorEvent.filter(
            pidor_id=pidor.id
        ).count()

    async def check_admin(self) -> bool:
        return True
        return await check_admin(
            bot,
            self.chat_id,
            self.user_id,
        )

    async def warn(self, *args, **kwargs):
        raise NotImplementedError


#     # warns: fields.ReverseRelation
#     # warned: fields.ReverseRelation


#     async def warn(self, victim: "Member", reason: str) -> Warn:
#         return await Warn.create(
#             who_warn_id=self.id,
#             who_warned_id=victim.id,
#             reason=reason,
#         )
