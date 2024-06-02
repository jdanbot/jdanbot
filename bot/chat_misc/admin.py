from functools import cached_property
import pytimeparse
from aiogram import types
from aiogram.filters import Command

from bot.config import bot

from ..config import router
from ..filters import IsAdmin, Check, GetText, Arguments
from ..database import Member
from pydantic import (
    BaseModel,
    BeforeValidator,
    AfterValidator,
    Field,
    ConfigDict,
)
from .lib.ban_logs import BanLog
import pendulum as pdl
from aiogram.utils.text_decorations import markdown_decoration as md
from typing import Annotated
from fluentogram import TranslatorRunner
from async_property import async_property, async_cached_property
from async_property.base import AsyncPropertyDescriptor
from async_property.cached import AsyncCachedPropertyDescriptor


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
    i18n: TranslatorRunner = Field(repr=False)


class BanHammer(BaseHammer):
    time: Annotated[int, BeforeValidator(pytimeparse.parse)] = 60
    reason: Annotated[str, AfterValidator(lambda x: x.strip())] = (
        "None"
    )

    @cached_property
    def until_duration(self) -> pdl.DateTime:
        return pdl.Duration(seconds=self.time)

    @cached_property
    def until(self) -> pdl.DateTime:
        return pdl.now() + self.until_duration


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
        return await (await self.member).warns.filter().count()

    @async_cached_property
    async def new_warn_counter(self) -> int:
        return await self.warn_counter + 1


@router.message(
    Command("mute"), IsAdmin(), Check("__enable_admin__"), Arguments()
)
async def admin_mute(
    message: types.Message, args: BanHammer, _: TranslatorRunner
):
    print(args)

    print(args.time)

    await message.chat.restrict(
        args.reply.from_user.id,
        until_date=args.until.timestamp(),
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

    print(_.get("admin_cant_unwarn_self"))
    print(_.get("mute"))
    print(log.generate())
    print(log.generate())

    await args.reply.reply(log.generate())


# @router.message(Command("selfmute", "selfban"))
# @handlers.check("__enable_admin__", "__enable_selfmute__")
# @handlers.parse_arguments_new
# async def selfmute(
#     message: types.Message,
#     time: CustomField(pytimeparse.parse, fallback=lambda x: int(x) / 60, default=1),
#     reason: CustomField(lambda x: str(x).strip(), default=lambda: _("ban.reason_not_found")),
# ):
#     action = BanHammer(message, message, time, reason)

#     if await action.execute():
#         await action.log()
#     else:
#         await message.reply(_("ban.selfmute_limit_reached"))


@router.message(
    Command("warn"), IsAdmin(), Check("__enable_admin__"), Arguments()
)
async def admin_warn(
    message: types.Message, args: WarnHammer, _: TranslatorRunner
):
    member = await Member.get_by(args.reply)
    admin = await Member.get_by(args.message)

    await args.new_warn_counter
    await admin.warn(member, reason=args.reason)

    await args.reply.reply(
        admin_log := _.warn_member(
            user=args.reply.from_user.mention_markdown(),
            admin=message.from_user.mention_markdown(),
            why=md.quote(args.reason) if args.reason else "null",
            i=await args.new_warn_counter,
        )
    )

    if message.chat.id == -1001176998310:
        await args.reply.forward(-1001334412934)
        await bot.send_message(-1001334412934, admin_log)

    await message.delete()

    if await args.new_warn_counter >= await args.warns_to_ban:
        await args.reply.reply("TOO MANY WARNS")


# @dp.message_handler(commands=["unwarn"], is_admin=True)
# @handlers.check("__enable_admin__")
# @parse_arguments_new
# async def admin_unwarn(
#     message: types.Message,
#     reply: types.Message,
#     reason: CustomField(str, default=lambda: _("ban.reason_not_found")),
# ):
#     if reply.from_user.id == message.from_user.id:
#         await message.reply(_("ban.admin_cant_unwarn_self"))
#         return

#     try:
#         action = UnwarnHammer(message, reply, reason)
#     except IndexError:
#         await message.reply(_("ban.warns_not_found"))
#         return

#     await action.execute()
#     await action.log()

#     if message.chat.id == -1001176998310:
#         await action.repost()


@router.message(Command("poll"), Check("enable_poll"), GetText())
async def kz_poll(message: types.Message, query: str):
    options = ["Да", "Нет", "Воздержусь"]
    is_katz_bots = False and message.chat.id == -1001334412934

    if is_katz_bots:
        options.append("Нет прав")

    await message.answer_poll(query, options, is_anonymous=False)
    await message.delete()


@router.message(Command("open"))
async def open_poll(message: types.Message):
    reply = message.reply_to_message.poll

    await message.answer_poll(
        reply.question,
        [option.text for option in reply.options],
        is_anonymous=False,
        allows_multiple_answers=reply.allows_multiple_answers,
    )
