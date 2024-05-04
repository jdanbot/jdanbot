from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import pendulum as pdl

from ...config import TIMEZONE, _, bot
from ...database import Member, Warn, Note
from .ban_logs import BanLog, BaseClass, UnwarnLog, WarnLog

from async_property import async_property


class BaseHammer(BaseClass):
    async def repost(self):
        await self.reply.forward(-1001334412934)
        await bot.send_message(
            -1001334412934, self.admin_log, parse_mode="MarkdownV2"
        )

    async def log(self):
        try:
            # await self.message.delete()
            await self.reply.reply(self.admin_log)
            await self.reply.reply(
                self.admin_log, parse_mode="MarkdownV2"
            )
        except Exception:
            await self.message.answer(
                self.admin_log, parse_mode="MarkdownV2"
            )


@dataclass
class BanHammer(BaseHammer):
    time: int
    reason: str

    def __post_init__(self):
        self.admin_log = BanLog(
            self.message,
            self.reply,
            self.reason,
            self.ban_time,
            self.until_date,
        ).generate()

    @property
    def is_selfmute(self) -> bool:
        return self.reply.from_user.id == self.message.from_user.id

    @property
    def ban_time(self) -> pdl.duration:
        return pdl.duration(seconds=max(30, min(31622400, self.time)))

    @property
    def until_date(self) -> pdl.datetime:
        return pdl.now(TIMEZONE) + self.ban_time

    async def execute(self):
        if self.is_selfmute and self.ban_time > pdl.duration(days=7):
            return False

        await self.message.chat.restrict(
            self.reply.from_user.id,
            until_date=self.until_date.timestamp(),
        )

        return True


@dataclass
class WarnHammer(BaseHammer):
    reason: str

    def __post_init__(self):
        self.admin_log = WarnLog(
            self.message,
            self.reply,
            self.reason,
            "FREIERPLATZ",
        ).generate()

    @property
    def warns_to_ban(self) -> int:
        try:
            return int(
                Note.get(self.message.chat.id, "__warns_to_ban__")
            )
        except Exception:
            return 3

    @async_property
    async def warn_counter(self) -> int:
        warned = await Member.get_by_message(self.reply)

        return await Warn.count_warns(warned.id)

    @async_property
    async def new_warn_counter(self) -> int:
        return await self.warn_counter + 1

    async def execute(self):
        await Warn.mark_chat_member(
            await Member.get_id_by(self.reply),
            await Member.get_id_by(self.message),
            reason=self.reason,
        )

        if await self.warn_counter >= self.warns_to_ban:
            action = BanHammer(
                self.message,
                self.reply,
                "1440",
                _(
                    "ban.warn_limit_reached",
                    i=await self.warn_counter,
                ),
            )

            await action.execute()
            await action.log()

            if self.message.chat.id == -1001176998310:
                await action.repost()


@dataclass
class UnwarnHammer(BaseHammer):
    reason: Optional[str] = None

    def __post_init__(self):
        self.warn_reason = self.user_warns[-1].reason
        self.admin_log = UnwarnLog(
            self.message,
            self.reply,
            self.warn_reason,
            self.warn_counter,
        ).generate()

    @property
    def user_warns(self) -> list[Warn]:
        warned = ChatMember.get_by_message(self.reply)

        return Warn.get_user_warns(warned.id)

    @property
    def warn_counter(self) -> int:
        warned = ChatMember.get_by_message(self.reply)

        return Warn.count_warns(warned.id)

    async def execute(self):
        admin = await Member.get_by(self.message)

        if len(self.user_warns) == 0:
            raise AttributeError()

        last_warn = self.user_warns[-1]
        Warn.update(
            who_unwarn_id=admin.id, unwarned_at=datetime.now(TIMEZONE)
        ).where(Warn.id == last_warn.id).execute()
