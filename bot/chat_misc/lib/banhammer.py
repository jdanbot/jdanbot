from cached_property import cached_property
from typing import Optional

import pendulum as pdl

from ...config import bot, TIMEZONE, _
from ...schemas import Warn, Note

from .ban_logs import BaseClass, BanLog, UnwarnLog, WarnLog


from dataclasses import dataclass


class BaseHammer(BaseClass):
    async def repost(self):
        await self.reply.forward(-1001334412934)
        await bot.send_message(-1001334412934, self.admin_log, parse_mode="MarkdownV2")

    async def log(self):
        try:
            await self.message.delete()
            await self.reply.reply(self.admin_log, parse_mode="MarkdownV2")
        except Exception:
            await self.message.answer(self.admin_log, parse_mode="MarkdownV2")


@dataclass
class BanHammer(BaseHammer):
    time: int
    reason: str

    def __post_init__(self):
        self.admin_log = BanLog(
            self.message, self.reply, self.reason, self.ban_time, self.until_date
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
            self.reply.from_user.id, until_date=self.until_date.timestamp()
        )

        return True


@dataclass
class WarnHammer(BaseHammer):
    reason: str

    def __post_init__(self):
        self.admin_log = WarnLog(
            self.message, self.reply, self.reason, self.new_warn_counter
        ).generate()

    @property
    def warns_to_ban(self) -> int:
        return Note.get(self.message.chat.id, "__warns_to_ban__", 3, int)

    @property
    def new_warn_counter(self) -> int:
        return self.user.warn_counter + 1

    async def execute(self):
        self.user.warn_by(self.admin, reason=self.reason)

        if self.user.warn_counter >= self.warns_to_ban:
            action = BanHammer(
                self.message,
                self.reply,
                "1440",
                _("ban.warn_limit_reached", i=self.user.warn_counter),
            )

            await action.execute()
            await action.log()

            if self.message.chat.id == -1001176998310:
                await action.repost()


@dataclass
class UnwarnHammer(BaseHammer):
    reason: Optional[str] = None

    @cached_property
    def old_warn(self) -> Warn:
        return self.user.warns[-1]

    @cached_property
    def warn_counter(self) -> int:
        return self.user.warn_counter

    @cached_property
    def admin_log(self) -> str:
        return UnwarnLog(
            self.message,
            self.reply,
            self.old_warn.reason,
            self.warn_counter
        ).generate()

    async def execute(self):
        if self.warn_counter == 0:
            raise IndexError()

        self.old_warn.unwarn_by(self.admin)
