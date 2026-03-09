from dataclasses import dataclass

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
    BaseModel,
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


class UnbanHammer(BaseHammer):
    reason: str = "None"


@router.message(
    Command("unmute"),
    IsAdmin(),
    Check("__enable_admin__"),
    Arguments(),
)
async def admin_unmute(
    message: types.Message,
    args: UnbanHammer,
    _: Locale,
):
    print(args)

    await message.chat.restrict(
        args.reply.from_user.id,
        until_date=30,
        use_independent_chat_permissions=False,
        permissions=types.ChatPermissions(),
    )
    await message.chat.restrict(
        args.reply.from_user.id,
        until_date=30,
        use_independent_chat_permissions=False,
        permissions=types.ChatPermissions(
            can_send_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_send_media_messages=True,
            can_add_web_page_previews=True,
        ),
    )

    await message.chat.unban(
        args.reply.from_user.id, only_if_banned=True
    )

    await args.reply.reply(admin_log := "UNMUTTED")

    if message.chat.id == -1001176998310:
        await args.reply.forward(-1001334412934)
        await bot.send_message(-1001334412934, admin_log)

    await message.delete()
