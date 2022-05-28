from aiogram import types
from aiogram.utils.markdown import escape_md
from dataclasses import dataclass
from datetime import datetime, timedelta

from ...lib.text import prettyword
from ...config import TIMEZONE, _


@dataclass
class BaseClass:
    message: types.Message
    reply: types.Message


@dataclass
class BanLog(BaseClass):
    reason: str
    ban_time: int
    until_date: timedelta

    @property
    def is_selfmute(self) -> bool:
        return self.reply.from_user.id == self.message.from_user.id

    @property
    def time_localed(self) -> str:
        return prettyword(self.ban_time, _("cases.minutes"))

    @property
    def unban_time(self) -> str:
        unban_time = self.until_date.isoformat(sep=" ").split(".")[0]

        now = datetime.now(TIMEZONE)
        one_day = now + timedelta(days=1)

        if one_day > self.until_date:
            return unban_time.split(" ")[1]

        return unban_time

    def generate(self) -> str:
        user, admin = self.reply.from_user, self.message.from_user

        return _(
            f"ban.{'mute' if not self.is_selfmute else 'selfmute'}",
            admin=escape_md(admin.full_name),
            admin_url=admin.url,

            **(dict(
                user=user.full_name,
                user_url=user.url
            ) if not self.is_selfmute else {}),

            why=escape_md(self.reason),
            time=str(self.ban_time),
            time_localed=self.time_localed,
            unban_time=escape_md(self.unban_time),
        )


@dataclass
class WarnLog(BaseClass):
    reason: str
    i: int

    def generate(self) -> str:
        user, admin = self.reply.from_user, self.message.from_user

        return _("ban.warn",
            user=escape_md(user.full_name),
            user_url=user.url,

            admin=escape_md(admin.full_name),
            admin_url=admin.url,

            why=escape_md(self.reason),
            i=self.i
        )


@dataclass
class UnwarnLog(BaseClass):
    reason: str
    i: int

    def generate(self) -> str:
        user, admin = self.reply.from_user, self.message.from_user

        return _("ban.unwarn",
            user=escape_md(user.full_name),
            user_url=user.url,

            admin=escape_md(admin.full_name),
            admin_url=admin.url,

            why=escape_md(self.reason),
            i=self.i
        )
