from aiogram import types
from dataclasses import dataclass
from datetime import datetime, timedelta

from .text import prettyword
from ..config import TIMEZONE, _


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
        return _(
            f"ban.{'mute' if not self.is_selfmute else 'selfmute'}",
            banchik=self.message.from_user.full_name,
            userid=self.reply.from_user.id,
            why=self.reason,
            time=str(self.ban_time),
            time_localed=self.time_localed,
            unban_time=self.unban_time,
            **(dict(name=self.reply.from_user.full_name) if not self.is_selfmute else {})
        )


@dataclass
class WarnLog(BaseClass):
    reason: str
    i: int

    def generate(self) -> str:
        return _(
            "ban.warn",
            name=self.reply.from_user.full_name,
            banchik=self.message.from_user.full_name,
            userid=self.message.from_user.id,
            why=self.reason,
            i=self.i
        )


@dataclass
class UnwarnLog(BaseClass):
    reason: str
    i: int

    def generate(self) -> str:
        return _(
            "ban.unwarn",
            name=self.reply.from_user.full_name,
            banchik=self.message.from_user.full_name,
            userid=self.message.from_user.id,
            i=self.i,
            why=self.reason
        )
