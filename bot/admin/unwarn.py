from dataclasses import dataclass

from aiogram import types
from aiogram.filters import Command
from aiogram.utils.text_decorations import (
    markdown_decoration as md,
)

from bot.config import bot

from ..config import Locale, router
from ..database import Member
from ..database.chat import ChatSettings
from ..filters import Arguments, Check, IsAdmin

escape_md = md.quote


@dataclass
class BaseClass:
    message: types.Message
    reply: types.Message
    _: Locale


class BaseHammer(BaseClass):
    async def repost(self):
        await self.reply.forward(-1001334412934)
        await bot.send_message(
            -1001334412934,
            self.admin_log,
            parse_mode="MarkdownV2",
        )

    async def log(self):
        try:
            # await self.message.delete()
            await self.reply.reply(self.admin_log)
            await self.reply.reply(
                self.admin_log, parse_mode="MarkdownV2"
            )
        except Exception:
            await self.message.answer(
                self.admin_log, parse_mode="MarkdownV2"
            )


@dataclass
class UnwarnHammer(BaseHammer):
    reason: Optional[str] = None

    def __post_init__(self):
        self.warn_reason = self.user_warns[-1].reason
        self.admin_log = UnwarnLog(
            self.message,
            self.reply,
            self.warn_reason,
            self.warn_counter,
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
        admin = await Member.get_by(self.message)

        if len(self.user_warns) == 0:
            raise AttributeError()

        last_warn = self.user_warns[-1]
        Warn.update(
            who_unwarn_id=admin.id,
            unwarned_at=datetime.now(TIMEZONE),
        ).where(Warn.id == last_warn.id).execute()


@dataclass
class UnwarnLog(BaseClass):
    reason: str
    i: int

    def generate(self) -> str:
        user, admin = (
            self.reply.from_user,
            self.message.from_user,
        )

        return self._.ban.unwarn(
            user=user.get_mention(),
            admin=admin.get_mention(),
            why=escape_md(self.reason),
            i=self.i,
        )


@router.message(
    Command("unwarn"),
    IsAdmin(),
    Check(ChatSettings.enable_admin),
    Arguments(),
)
async def admin_unwarn(
    message: types.Message,
    reply: types.Message,
    reason: CustomField(
        str, default=lambda: _("ban.reason_not_found")
    ),
):
    if reply.from_user.id == message.from_user.id:
        await message.reply(_("ban.admin_cant_unwarn_self"))
        return

    try:
        action = UnwarnHammer(message, reply, reason)
    except IndexError:
        await message.reply(_("ban.warns_not_found"))
        return

    await action.execute()
    await action.log()

    if message.chat.id == -1001176998310:
        await action.repost()
