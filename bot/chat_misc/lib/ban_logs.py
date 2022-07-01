import humanize

from aiogram import types
from aiogram.utils.markdown import escape_md
from dataclasses import dataclass

import pendulum as pdl

from ...config import _


@dataclass
class BaseClass:
    message: types.Message
    reply: types.Message


@dataclass
class BanLog(BaseClass):
    reason: str
    ban_time: pdl.duration
    until_date: pdl.datetime

    @property
    def is_selfmute(self) -> bool:
        return self.reply.from_user.id == self.message.from_user.id

    @property
    def time_localed(self) -> str:
        lang = _(None, return_lang=True)
        humanize.i18n.activate(None if lang == "en" else lang)

        return humanize.precisedelta(self.ban_time)

    @property
    def unban_time(self) -> str:
        if self.ban_time >= pdl.duration(days=1):
            return "{} {}".format(
                self.until_date.to_formatted_date_string(),
                self.until_date.to_time_string()
            )
        else:
            return self.until_date.to_time_string()

    def generate(self) -> str:
        user, admin = self.reply.from_user, self.message.from_user

        return _(
            f"ban.{'mute' if not self.is_selfmute else 'selfmute'}",
            admin=admin.get_mention(),

            **(dict(
                user=user.get_mention()
            ) if not self.is_selfmute else {}),

            why=escape_md(self.reason),
            time=self.time_localed,
            unban_time=escape_md(self.unban_time),
        )


@dataclass
class WarnLog(BaseClass):
    reason: str
    i: int

    def generate(self) -> str:
        user, admin = self.reply.from_user, self.message.from_user

        return _("ban.warn",
            user=user.get_mention(),
            admin=admin.get_mention(),

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
            user=user.get_mention(),
            admin=admin.get_mention(),

            why=escape_md(self.reason),
            i=self.i
        )
