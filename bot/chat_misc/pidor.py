import asyncio
from random import choice

from aiogram import types
from aiogram.filters import Command
from aiogram.utils.markdown import bold, italic

from bot.database.member import Member
from bot.database.pidor import Pidor

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
    if await member.check_pidor_is_runnable():
        return True
    else:
        pidor = await Pidor.get(
            id=member.chat.current_pidor_id
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
    _: Locale,
    member: Member,
    ignore_pidor_wait: bool = False,
):
    if not await init_pidor(message, member, _=_):
        return

    random_member: Member = await member.get_random_pidor()

    if await random_member.is_left():
        await message.reply(_.pidor.pidor_left)
        return

    await random_member.become_today_pidor()

    for phrase in choice(_.pidor.pidor_searching):
        if phrase != "\n":
            await message.answer(italic(phrase))
        if not ignore_pidor_wait:
            await asyncio.sleep(2.5)

    await message.answer(
        choice(_.pidor.today_pidor)(
            user=bold(random_member.tag),
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
    count = await member.get_pidor_count()

    if count == 0:
        await message.reply(_.pidor.stats_unavailable)
        return

    for num, pidor in enumerate(
        await member.get_top_pidors(), 1
    ):
        count = prettyword(pidor.count, _.cases)

        msg += PIDOR_TEMPLATE.format(
            get_emojed_num(num),
            pidor.full_name,
            pidor.count,
            count,
        )

    msg += "\n"
    msg += _.pidor.total_members(count=count)

    await message.reply(
        msg,
        parse_mode="Markdown",
    )


@router.message(Command("pidorreg", "pidoreg"))
async def reg_pidor(
    message: types.Message, _: Locale, member: Member
) -> None:
    __, is_created = await member.get_pidor()

    await message.reply(
        _.pidor.in_db
        if is_created
        else _.pidor.already_in_db,
        parse_mode="Markdown",
    )
