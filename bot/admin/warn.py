from dataclasses import dataclass

from aiogram import types
from aiogram.filters import Command
from aiogram.utils.text_decorations import (
    markdown_decoration as md,
)
from async_property import (
    async_cached_property,
    async_property,
)
from async_property.base import AsyncPropertyDescriptor
from async_property.cached import (
    AsyncCachedPropertyDescriptor,
)
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from bot.config import bot

from ..config import Locale, router
from ..database import Member
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


class WarnHammer(BaseHammer):
    reason: str | None = None

    @async_property
    async def warns_to_ban(self) -> int:
        return 3

    @async_cached_property
    async def member(self) -> Member:
        return await Member.get_by(self.reply)

    @async_cached_property
    async def warn_counter(self) -> int:
        return 0
        # return await (await self.member).warns.filter().count()

    @async_cached_property
    async def new_warn_counter(self) -> int:
        return await self.warn_counter + 1


@dataclass
class WarnLog(BaseClass):
    reason: str
    i: int

    def generate(self) -> str:
        user, admin = (
            self.reply.from_user,
            self.message.from_user,
        )

        return self._.ban.warn(
            user=user.get_mention(),
            admin=admin.get_mention(),
            why=escape_md(self.reason),
            i=self.i,
        )


@router.message(
    Command("warn"),
    IsAdmin(),
    Check("__enable_admin__"),
    Arguments(),
)
async def admin_warn(
    message: types.Message,
    args: WarnHammer,
    _: Locale,
):
    member = await Member.get_by(args.reply)
    admin = await Member.get_by(args.message)

    await args.new_warn_counter
    # await admin.warn(member, reason=args.reason)

    await args.reply.reply(
        admin_log := _.ban.warn(
            user=args.reply.from_user.mention_markdown(),
            admin=message.from_user.mention_markdown(),
            why=md.quote(args.reason)
            if args.reason
            else "null",
            i=await args.new_warn_counter,
        )
    )

    if message.chat.id == -1001176998310:
        await args.reply.forward(-1001334412934)
        await bot.send_message(
            -1001334412934, admin_log, parse_mode="Markdown"
        )

    await message.delete()

    if (
        await args.new_warn_counter
        >= await args.warns_to_ban
    ):
        await args.reply.reply("TOO MANY WARNS")
