import dataclasses
from typing import Optional

from aiogram import types
from datetime import datetime, timedelta

import math

from ..config import bot, TIMEZONE, _
from ..database import Warn, ChatMember, Note

from .ban_logs import BaseClass, BanLog, UnwarnLog, WarnLog


from dataclasses import dataclass


class BaseHammer(BaseClass):
    async def repost(self):
        await self.reply.forward(-1001334412934)
        await bot.send_message(-1001334412934, self.admin_log, parse_mode="MarkdownV2")

    async def log(self):
        try:
            await self.reply.reply(self.admin_log, parse_mode="MarkdownV2")
            await self.message.delete()
        except:
            await self.message.reply(self.admin_log, parse_mode="MarkdownV2")


@dataclass
class BanHammer(BaseHammer):
    time: int | str = 1
    reason: Optional[str] = None

    def __post_init__(self):
        if self.is_selfmute and int(self.time) > 10080 \
            and self.message.chat == -1001334412934:
            self.time = 10080

        self.admin_log = BanLog(
            self.message,
            self.reply,
            self.reason or _("ban.reason_not_found"),
            self.ban_time,
            self.until_date
        ).generate()

    @property
    def is_selfmute(self) -> bool:
        return self.reply.from_user.id == self.message.from_user.id

    @property
    def ban_time(self) -> int:
        try:
            return max(1, math.ceil(float(self.time)))

        except ValueError:
            bt = datetime.time.fromisoformat(self.time)
            return bt.hour * 60 + bt.minute

    @property
    def until_date(self) -> timedelta:
        return datetime.now(TIMEZONE) + timedelta(minutes=self.ban_time)

    async def execute(self):
        await self.message.chat.restrict(
            self.reply.from_user.id,
            until_date=self.until_date.timestamp()
        )


@dataclass
class WarnHammer(BaseHammer):
    reason: Optional[str] = None

    def __post_init__(self):
        self.reason = self.reason or _("ban.reason_not_found")

        self.admin_log = WarnLog(
            self.message,
            self.reply,
            self.reason,
            self.new_warn_counter
        ).generate()

    @property
    def warns_to_ban(self) -> int:
        try:
            return int(Note.get(self.message.chat.id, "__warns_to_ban__"))
        except Exception:
            return 3

    @property
    def warn_counter(self) -> int:
        warned = ChatMember.get_by_message(self.reply)

        return Warn.count_warns(warned.id)

    @property
    def new_warn_counter(self) -> int:
        return self.warn_counter + 1

    async def execute(self):
        Warn.mark_chat_member(
            ChatMember.get_by_message(self.reply).id,
            ChatMember.get_by_message(self.message).id,
            reason=self.reason
        )

        if self.warn_counter >= self.warns_to_ban:
            action = BanHammer(
                self.message,
                self.reply,
                "1440",
                _("ban.warn_limit_reached", i=self.warn_counter)
            )

            await action.execute()
            await action.log()

            if self.message.chat.id == -1001176998310:
                await action.repost()


@dataclass
class UnwarnHammer(BaseHammer):
    reason: Optional[str] = None

    def __post_init__(self):
        self.reason = self.reason or _("ban.reason_not_found")
        self.warn_reason = self.user_warns[-1].reason

        self.admin_log = UnwarnLog(
            self.message,
            self.reply,
            self.warn_reason,
            self.warn_counter
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
        admin = ChatMember.get_by_message(self.message)

        if len(self.user_warns) == 0:
            raise AttributeError()

        last_warn = self.user_warns[-1]
        Warn.update(
            who_unwarn_id=admin.id,
            unwarned_at=datetime.now(TIMEZONE)
        ).where(Warn.id == last_warn.id).execute()
