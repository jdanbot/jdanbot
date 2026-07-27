from datetime import datetime, timedelta
from itertools import chain
from typing import Any, override
from zoneinfo import ZoneInfo

from aiogram import types
from aiogram.utils.markdown import hlink, link
from msgspec import Struct, convert
from pypika import Field, Order, Query
from pypika import functions as fn

from ..config.bot import COMMANDS, bot
from ..config.config import settings
from ..lib.admin import check_admin
from ._base import BetterConnection, dbmethod
from ._extras import IsInserted, Unixepoch
from ._tables import CMD, C, E, M, P, U, W
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

        await Member.safe_create(chat, user, conn=conn)
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

    @dbmethod
    @staticmethod
    async def safe_create(
        chat: Chat, user: User, *, conn: BetterConnection
    ):
        from pypika import PostgreSQLQuery as Query

        await conn.execute_raw(
            Query.into(M)  # type: ignore[operator]
            .columns(M.chat_id, M.user_id)
            .insert(chat.id, user.id)
            .on_conflict(M.chat_id, M.user_id)
            .do_nothing()
        )
        await conn.commit()

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

    @staticmethod
    def status_to_emoji(status: str) -> str:
        match status:
            case "creator":
                return "🤴"
            case "administrator":
                return "👮‍♂️"
            case "member":
                return "🥸"
            case _:
                return "🌚"

    async def get_status_emoji(self) -> str:
        status = await self.get_status()

        return self.status_to_emoji(
            status
            if self.user_id not in settings.bot_owners
            else "owner"
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
        return await conn.execute_scalar(
            Query.from_(P)
            .select(1)
            .where(P.chat_id == self.chat_id)
            .where(P.user_id == self.user_id)
            .where(P.is_allowed)
        )

    @dbmethod
    async def get_pidor(
        self, conn: BetterConnection
    ) -> tuple[Pidor, bool]:
        from pypika import PostgreSQLQuery as Query

        _ = await conn.execute_one(
            Query.into(P)  # type: ignore[operator]
            .columns(P.chat_id, P.user_id)
            .insert(self.chat_id, self.user_id)
            .on_conflict(P.chat_id, P.user_id)
            .do_update(P.chat_id, self.chat_id)
            .returning(
                P.id,
                P.chat_id,
                P.user_id,
                P.is_allowed,
                P.latest_time,
                IsInserted(),
            )
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
        from pypika import PostgreSQLQuery as Query

        event_id = await conn.execute_scalar(
            Query.into(E)  # type: ignore[operator]
            .columns(E.chat_id, E.pidor_id)
            .insert(self.chat_id, self.user_id)
            .returning(E.id)
        )

        await conn.execute_many(
            Query.update(P)
            .set(P.latest_time, event_id)
            .where(P.id == self.pidor.id),
            Query.update(C)
            .set(C.pidor_id, self.pidor.id)
            .where(C.id == self.chat_id),
        )

        await conn.commit()

    @dbmethod
    async def get_random_pidor(
        self, conn: BetterConnection
    ) -> "Member":
        _ = await conn.execute_one(
            Query.from_(P)
            .select(
                P.id,
                P.chat_id,
                P.user_id,
                P.is_allowed,
                P.latest_time,
            )
            .where(P.chat_id == self.chat_id)
            .where(P.is_allowed == 1)
            .orderby("random()")
            .limit(1)
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
        return await conn.execute_scalar(
            Query.from_(P)
            .select(fn.Count("*"))
            .where(P.chat_id == self.chat_id)
        )

    @dbmethod
    async def get_top_pidors(
        self,
        limit: int = 10,
        *,
        conn: BetterConnection,
    ) -> PidorTop:
        _ = await conn.execute_all(
            Query.from_(E)
            .select(
                fn.Count(E.id).as_("events_count"),
                U.first_name,
                U.last_name,
                U.username,
            )
            .join(P)
            .on(P.id == E.pidor_id)
            .join(U)
            .on(U.id == P.user_id)
            .where(E.chat_id == self.chat_id)
            .where(P.is_allowed == 1)
            .groupby(U.id)
            .orderby(
                Field("events_count"), order=Order.desc
            )
            .limit(limit)
        )
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

    @dbmethod
    async def get_pidor_count_here(
        self, conn: BetterConnection
    ) -> int:
        return await conn.execute_scalar(
            Query.from_(E)
            .select(fn.Count("*"))
            .join(P)
            .on(E.pidor_id == P.id)
            .where(E.chat_id == self.chat_id)
            .where(P.user_id == self.user_id)
        )

    @dbmethod
    async def get_pidor_count_anywhere(
        self, conn: BetterConnection
    ) -> int:
        return await conn.execute_scalar(
            Query.from_(E)
            .select(fn.Count("*"))
            .join(P)
            .on(E.pidor_id == P.id)
            .where(P.user_id == self.user_id)
        )

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

    ############  SPY  ############
    @dbmethod
    async def get_members_count(
        self, conn: BetterConnection
    ) -> int:
        return await conn.execute_scalar(
            Query.from_(M)
            .select(fn.Count("*"))
            .where(M.chat_id == self.chat.id)
        )

    @dbmethod
    async def get_chat_commands_count(
        self, conn: BetterConnection
    ) -> int:
        return await conn.execute_scalar(
            Query.from_(CMD)
            .select(fn.Count("*"))
            .where(CMD.chat_id == self.chat.id)
        )

    @dbmethod
    async def features_used(
        self, conn: BetterConnection
    ) -> int:
        _ = await conn.execute_all(
            Query.from_(CMD)
            .select(CMD.name)
            .distinct()
            .where(CMD.user_id == self.user_id)
        )

        user_commands = list(chain.from_iterable(_))

        CMDS = COMMANDS.listed
        USER = sum(
            any(
                command in user_commands
                for command in command_variants
            )
            for command_variants in CMDS
        )

        return int(USER / len(CMDS) * 100)

    @dbmethod
    async def has_chats(self, conn: BetterConnection):
        return await conn.execute_scalar(
            Query.from_(M)
            .select(fn.Count("*"))
            .where(M.user_id == self.user_id)
        )

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
            .set(W.unwarned_at, Unixepoch())
            .where(W.id == get_latest_warn)
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
                "strftime('%s', datetime('now', '-24 hours'))",
            )
        )
        return _
