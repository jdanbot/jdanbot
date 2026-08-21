import asyncio
from random import choice

from aiogram import types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.utils.markdown import bold, italic

from bot.database.member import Member
from bot.database.pidor import Pidor

from ..config import is_test_session
from ..config.bot import router
from ..config.lib.locales import Locale
from ..database._base import BetterConnection, dbmethod
from ..lib.text import prettyword


@dbmethod
async def init_pidor(
    message: types.Message,
    member: Member,
    conn: BetterConnection,
    _: Locale,
) -> bool:
    if message.chat.id > 0:
        await message.reply(_.pidor.works_only_in_chats)
        return False

    if not await member.is_pidor(conn=conn):
        await message.reply(
            _.pidor.reg, parse_mode="Markdown"
        )
        return False

    # Should we start finding of a pidor?
    if await member.check_pidor_is_runnable(conn=conn):
        return True
    else:
        pidor = await Pidor.get(
            id=member.chat.current_pidor_id, conn=conn
        )

        mem = await Member.get(
            pidor.user_id, pidor.chat_id, conn=conn
        )

        await message.reply(
            choice(
                _.pidor.already_finded,
            ).format(
                user=bold(mem.mention),
            )
        )
        return False


@router.message(Command("pidor"))
async def find_pidor(
    message: types.Message,
    member: Member,
    _: Locale,
):
    if not await init_pidor(message, member, _=_):
        return

    random_member: Member = await member.get_random_pidor()

    try:
        is_member_left = await random_member.is_left()
    except TelegramBadRequest:
        is_member_left = None

    if not is_member_left is False:
        await message.reply(
            _.pidor.pidor_left, parse_mode=None
        )
        await random_member.change_pidor_agreement(False)
        return

    await random_member.become_today_pidor()

    for phrase in choice(_.pidor.pidor_searching):
        if phrase != "\n":
            await message.answer(italic(phrase))
        if not is_test_session:
            await asyncio.sleep(2.5)

    await message.answer(
        choice(_.pidor.today_pidor)(
            user=f"*{random_member.tag}*",
        )
    )


PIDOR_TEMPLATE = "_{}_ *{}* — `{}` {}\n"


def get_emojed_num(num: int) -> str:
    return ["🥇", "🥈", "🥉", f"{num}."][min(num - 1, 3)]


@router.message(Command("pidorstats"))
async def pidor_stats(
    message: types.Message,
    member: Member,
    _: Locale,
):
    msg = _.pidor.top_10 + "\n\n"
    chat_count = await member.get_pidor_count()

    if chat_count == 0:
        await message.reply(_.pidor.stats_unavailable)
        return

    for num, pidor in enumerate(
        await member.get_top_pidors(), 1
    ):
        count = prettyword(pidor.count, _.cases.times)

        msg += PIDOR_TEMPLATE.format(
            get_emojed_num(num),
            pidor.full_name,
            pidor.count,
            count,
        )

    msg += "\n"
    msg += _.pidor.total_members(
        count=f"{chat_count} {prettyword(chat_count, _.cases.members)}",
    )

    await message.reply(
        msg,
        parse_mode="Markdown",
    )


@router.message(Command("pidorreg", "pidoreg"))
async def reg_pidor(
    message: types.Message, _: Locale, member: Member
) -> None:
    __, is_created = await member.get_pidor()

    if not __.is_allowed:
        await member.change_pidor_agreement(True)

    await message.reply(
        _.pidor.in_db
        if is_created
        else (
            _.pidor.already_in_db
            if __.is_allowed
            else _.pidor.rejoin_in_game
        ),
        parse_mode="Markdown",
    )
