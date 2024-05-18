import pytimeparse
from aiogram import types
from aiogram.filters import Command

from ..config import router
from ..filters import IsAdmin, Check, GetText, Arguments
from pydantic import BaseModel, BeforeValidator, AfterValidator, Field
from typing import Annotated


class BaseHammer(BaseModel):
    message: types.Message = Field(repr=False)
    reply: types.Message | None = Field(repr=False)


class BanHammer(BaseHammer):
    time: Annotated[int, BeforeValidator(pytimeparse.parse)] = 60
    reason: Annotated[str, AfterValidator(lambda x: x.strip())] = (
        "None"
    )


@router.message(
    Command("mute"), IsAdmin(), Check("__enable_admin__"), Arguments()
)
async def admin_mute(message: types.Message, args: BanHammer):
    print(args)
    action = BanHammer(message, reply, time, reason)

    await action.execute()
    await action.log()

    if message.chat.id == -1001176998310:
        await action.repost()


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


# @dp.message_handler(commands=["warn"], is_admin=True)
# @handlers.check("__enable_admin__")
# @parse_arguments_new
# async def admin_warn(
#     message: types.Message,
#     reply: types.Message,
#     reason: CustomField(str, default=lambda: _("ban.reason_not_found")),
# ):
#     action = WarnHammer(message, reply, reason)

#     await action.log()
#     await action.execute()

#     if message.chat.id == -1001176998310:
#         await action.repost()


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

    poll = await message.answer_poll(
        query, options, is_anonymous=False
    )

    if is_katz_bots:
        await poll.pin(disable_notification=True)
        Poll.insert(
            id=poll.message_id,
            author_id=ChatMember.get_by_message(message).id,
            description=query,
        ).execute()

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
