from datetime import datetime, timedelta
from typing import Any, override
from zoneinfo import ZoneInfo

from aiogram import types
from aiogram.utils.markdown import hlink, link
from msgspec import Struct, convert
from pypika import Order, Query
from pypika import functions as fn

from ..config.bot import bot
from ..lib.admin import check_admin
from ._base import BetterConnection, dbmethod, queries
from ._tables import P, W
from .chat import Chat
from .pidor import Pidor, PidorTop
from .user import User

MSK = ZoneInfo("Europe/Moscow")


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
        print(self)
        print(self.username)
        if self.username:
            return f"@{self.username}"

        return (hlink if use_html else link)(
            self.full_name,
            f"tg://user?id={self.user_id}",
        )

    @dbmethod
    @staticmethod
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
        *,
        conn: BetterConnection,
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
            convert(_[:-1], Pidor),
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

        pidor = convert(_, Pidor)

        return await Member.get(
            conn=conn,
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
        *,
        conn: BetterConnection,
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

    @dbmethod
    async def check_pidor_is_runnable(
        self, conn: BetterConnection
    ) -> bool:
        if self.chat.current_pidor_id is None:
            return True

        pidor: Pidor = await Pidor.get(
            id=self.chat.current_pidor_id, conn=conn
        )

        date = await pidor.get_latest_datetime(conn=conn)
        next_pidor_day = date + timedelta(days=1)

        return datetime.now(MSK).date() >= next_pidor_day

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

    @dbmethod
    async def change_pidor_agreement(
        self, value: bool, *, conn: BetterConnection
    ):
        await conn.execute_raw(
            Query.update(P)
            .set(P.is_allowed, value)
            .where(P.chat_id == self.chat_id)
            .where(P.user_id == self.user_id)
        )
        await conn.commit()

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
        await conn.execute_one(
            Query.into(W)
            .columns(
                W.chat_id,
                W.victim_id,
                W.warn_admin_id,
                W.reason,
            )
            .insert(
                self.chat_id,
                user.user_id,
                self.user_id,
                reason,
            )
        )
        await conn.commit()

        return await user.get_warn_count(conn=conn)

    @dbmethod
    async def unwarn(
        self,
        user: "Member",
        reason: str,
        conn: BetterConnection,
    ) -> int:
        _ = await user.get_warn_count(conn=conn)

        if _ == 0:
            raise IndexError

        get_latest_warn = (
            Query.from_(W)
            .select(W.id)
            .where(
                (W.chat_id == self.chat_id)
                & (W.victim_id == user.user_id)
                & (W.unwarned_at.isnull())
            )
            .orderby(W.warned_at, order=Order.desc)
            .limit(1)
        )

        await conn.execute_one(
            Query.update(W)
            .set(W.unwarn_admin_id, self.user_id)
            .set(W.unwarn_reason, reason)
            .set(W.unwarned_at, fn.Now())
            .where(W.id == get_latest_warn)
            .get_sql()
            .replace("NOW()", "unixepoch()")
        )
        await conn.commit()

        return _

    @dbmethod
    async def get_warn_count(
        self, conn: BetterConnection
    ) -> int:
        _ = await conn.execute_scalar(
            Query.from_(W)
            .select(fn.Count(W.id))
            .where(
                (W.chat_id == self.chat_id)
                & (W.victim_id == self.user_id)
                & (W.unwarned_at.isnull())
                & (W.warned_at > fn.Now())
            )
            .get_sql()
            .replace(
                "NOW()",
                "datetime(CURRENT_TIMESTAMP, '-24 hours')",
            )
        )
        return _
