from dataclasses import dataclass

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
    BaseModel,
    ConfigDict,
    Field,
)

from ..config import Locale, router
from ..filters import Arguments, Check

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


@router.message(
    Command("selfmute", "selfban"),
    Check("__enable_admin__", "__enable_selfmute__"),
    Arguments(),
)
async def selfmute(
    message: types.Message,
    time: CustomField(
        pytimeparse.parse,
        fallback=lambda x: int(x) / 60,
        default=1,
    ),
    reason: CustomField(
        lambda x: str(x).strip(),
        default=lambda: _("ban.reason_not_found"),
    ),
):
    action = BanHammer(message, message, time, reason)

    if await action.execute():
        await action.log()
    else:
        await message.reply(_("ban.selfmute_limit_reached"))
