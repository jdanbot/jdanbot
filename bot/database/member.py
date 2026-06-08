from typing import Any, override

from aiogram import types
from aiogram.utils.markdown import hlink, link
from msgspec import Struct, convert
from pypika import Order, Query, Table
from pypika import functions as fn
from whenever import Instant, Time

from ..config.bot import bot
from ..lib.admin import check_admin
from ._base import BetterConnection, dbmethod, queries
from .chat import Chat
from .pidor import Pidor, PidorTop
from .user import User


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
    pidor: Pidor | None = None

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

    @dbmethod
    async def get_by(
        message: types.Message,
        conn: BetterConnection,
    ) -> "Member":
        chat: Chat = await Chat.get_by(message, conn=conn)
        user: User = await User.get_by(message, conn=conn)

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
        pidor: Pidor | None = None,
        conn: BetterConnection = None,
    ) -> "Member":
        chat: Chat = await Chat.get(id=chat_id, conn=conn)
        user: User = await User.get(id=user_id, conn=conn)

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

    @dbmethod
    async def is_pidor(
        self, conn: BetterConnection
    ) -> bool:
        return await queries.pidor.check_is_pidor(
            conn,
            chat_id=self.chat_id,
            user_id=self.user_id,
        )

    @dbmethod
    async def get_pidor(
        self, conn: BetterConnection
    ) -> tuple[Pidor, bool]:
        _ = await queries.pidor.get_or_create(
            conn,
            chat_id=self.chat_id,
            user_id=self.user_id,
        )
        await conn.commit()

        return (
            convert(_, Pidor),
            bool(_[-1]),
        )

    @dbmethod
    async def become_today_pidor(
        self, conn: BetterConnection
    ):
        assert self.pidor is not None, "???"

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

    @dbmethod
    async def get_random_pidor(
        self, conn: BetterConnection
    ) -> "Member":
        _ = await queries.pidor.get_random_pidor(
            conn, chat_id=self.chat_id
        )

        if _ is None:
            raise KeyError
        print(_)

        pidor = convert(
            (
                *_[:-2],
                bool(_[-2]),
                _[-1],
            ),
            Pidor,
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

    @dbmethod
    async def get_pidor_count(
        self, conn: BetterConnection
    ) -> int:
        return await queries.pidor.get_pidor_members_count(
            conn, chat_id=self.chat_id
        )

    @dbmethod
    async def get_top_pidors(
        self,
        limit: int = 10,
        conn: BetterConnection = None,
    ) -> PidorTop:
        _ = [
            i
            async for i in queries.pidor.get_top(
                conn,
                chat_id=self.chat_id,
                limit=limit,
            )
        ]

        return convert(_, PidorTop)

    async def check_run_pidor(self) -> bool:
        if self.chat.current_pidor_id is None:
            return True
        print(self.chat.current_pidor_id)
        print("!!!!")

        pidor: Pidor = await Pidor.get(
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
        return await PidorEvent.filter(  # noqa
            pidor_id=pidor.id
        ).count()

    ############ ADMIN ############

    async def check_admin(self) -> bool:
        return await check_admin(
            bot,
            self.chat_id,
            self.user_id,
        )

    @dbmethod
    async def warn(
        self,
        user: "Member",
        reason: str,
        conn: BetterConnection,
    ) -> int:
        w = Table("warns")

        await conn.execute_one(
            Query.into(w)
            .columns(
                w.chat_id,
                w.victim_id,
                w.warn_admin_id,
                w.reason,
            )
            .insert(
                self.chat_id,
                user.user_id,
                self.user_id,
                reason,
            )
        )
        await conn.execute_one(Query.into(w).insert())
        await conn.commit()

        return await user.get_warn_count(conn=conn)

    @dbmethod
    async def unwarn(
        self,
        user: "Member",
        reason: str,
        conn: BetterConnection,
    ) -> int:
        _ = await user.get_warn_count()

        if _ == 0:
            raise IndexError

        w = Table("warns")

        get_latest_warn = (
            Query.from_(w)
            .select(w.id)
            .where(
                (w.chat_id == self.chat_id)
                & (w.victim_id == user.user_id)
                & (w.unwarned_at.isnull())
            )
            .orderby(w.warned_at, order=Order.desc)
            .limit(1)
        )

        await conn.execute_one(
            Query.update(w)
            .set(w.unwarn_admin_id, self.user_id)
            .set(w.unwarn_reason, reason)
            .set(w.unwarned_at, fn.Now())
            .where(w.id == get_latest_warn)
            .get_sql()
            .replace("NOW()", "CURRENT_TIMESTAMP")
        )
        await conn.commit()

        return _

    @dbmethod
    async def get_warn_count(
        self, conn: BetterConnection
    ) -> int:
        w = Table("warns")
        _ = await conn.execute_scalar(
            Query.from_(w)
            .select(fn.Count(w.id))
            .where(
                (w.chat_id == self.chat_id)
                & (w.victim_id == self.user_id)
                & (w.unwarned_at.isnull())
                & (w.warned_at > fn.Now())
            )
            .get_sql()
            .replace(
                "NOW()",
                "datetime(CURRENT_TIMESTAMP, '-24 hours')",
            )
        )
        return _
