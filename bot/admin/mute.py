from dataclasses import dataclass
from functools import cached_property
from typing import Annotated

import humanize
import pendulum as pdl
import pytimeparse2 as pytimeparse
from aiogram import types
from aiogram.filters import Command
from aiogram.utils.text_decorations import (
    markdown_decoration as md,
)
from async_property.base import AsyncPropertyDescriptor
from async_property.cached import (
    AsyncCachedPropertyDescriptor,
)
from pydantic import (
    AfterValidator,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
)

from bot.config import bot

from ..config import Locale, router
from ..filters import Arguments, Check, IsAdmin

escape_md = md.quote


class BaseHammer(BaseModel):
    model_config = ConfigDict(
        ignored_types=(
            AsyncPropertyDescriptor,
            AsyncCachedPropertyDescriptor,
        ),
        arbitrary_types_allowed=True,
    )

    message: types.Message = Field(repr=False)
    reply: types.Message | None = Field(repr=False)
    i18n: Locale = Field(repr=False)


@dataclass
class BaseClass:
    message: types.Message
    reply: types.Message
    _: Locale


class BanHammer(BaseHammer):
    time: Annotated[
        int, BeforeValidator(pytimeparse.parse)
    ] = 60
    reason: Annotated[
        str, AfterValidator(lambda x: x.strip())
    ] = "None"

    @cached_property
    def until_duration(self) -> pdl.Duration:
        return pdl.Duration(seconds=self.time)

    @cached_property
    def until(self) -> pdl.DateTime:
        return pdl.now() + self.until_duration


@dataclass
class BanLog(BaseClass):
    reason: str
    ban_time: pdl.Duration
    until_date: pdl.DateTime

    @property
    def is_selfmute(self) -> bool:
        return (
            self.reply.from_user.id
            == self.message.from_user.id
        )

    @property
    def time_localed(self) -> str:
        lang = self._.lang
        humanize.i18n.activate(
            None if lang == "en" else lang
        )

        return humanize.precisedelta(self.ban_time)

    @property
    def unban_time(self) -> str:
        if self.ban_time >= pdl.duration(days=1):
            return "{} {}".format(
                self.until_date.to_formatted_date_string(),
                self.until_date.to_time_string(),
            )
        else:
            return self.until_date.to_time_string()

    def generate(self) -> str:
        user, admin = (
            self.reply.from_user,
            self.message.from_user,
        )

        return (
            self._.ban.mute
            if not self.is_selfmute
            else self._.ban.selfmute
        )(
            admin=admin.mention_markdown(),
            **(
                dict(user=user.mention_markdown())
                if not self.is_selfmute
                else {}
            ),
            why=escape_md(self.reason),
            time=self.time_localed,
            unban_time=escape_md(self.unban_time),
        )


@router.message(
    Command("mute"),
    IsAdmin(),
    Check("__enable_admin__"),
    Arguments(),
)
async def admin_mute(
    message: types.Message,
    args: BanHammer,
    _: Locale,
):
    assert args.reply
    assert args.reply.from_user
    print(args)

    print(args.time)

    message.chat.restrict(
        args.reply.from_user.id,
        until_date=args.until.timestamp().__int__(),
        permissions=types.ChatPermissions(),
    )

    log = BanLog(
        message,
        args.reply,
        _,
        args.reason,
        args.until_duration,
        args.until,
    )

    await args.reply.reply(admin_log := log.generate())

    if message.chat.id == -1001176998310:
        await args.reply.forward(-1001334412934)
        await bot.send_message(-1001334412934, admin_log)

    await message.delete()
