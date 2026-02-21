import asyncio
from random import choice

from aiogram import types
from aiogram.filters import Command
from aiogram.utils.markdown import bold, italic

from bot.database.member import Member
from bot.database.pidor import Pidor, PidorEvent

from ..config.bot import router
from ..config.lib.locales import Locale
from ..database import Member, PidorEvent
from ..lib.text import prettyword


async def init_pidor(
    message: types.Message,
    member: Member,
    _: Locale,
) -> bool:
    if message.chat.id > 0:
        await message.reply(_.pidor.works_only_in_chats)
        return False

    if not await member.is_pidor():
        await message.reply(_.pidor.reg)
        return False

    if not await member.check_run_pidor():
        pidor = await Pidor.get(id=member.chat.pidor_id)
        mem = await Member.get(pidor.user_id, pidor.chat_id)

        await message.reply(
            choice(
                _.pidor.already_finded,
            ).format(
                user=bold(mem.mention),
            )
        )
        return False

    return True


@router.message(Command("pidor"))
async def find_pidor(
    message: types.Message,
    _: Locale,
    ignore_pidor_wait: bool = False,
):
    member: Member = await Member.get_by(message)

    if not await init_pidor(message, member, _):
        return

    pidor, __ = await member.get_pidor()

    await PidorEvent.create(
        pidor_id=pidor.id,
        chat_id=member.chat_id,
    )

    new_pidor: Pidor = await member.get_random_pidor()
    new_member: Member = await Member.get(
        user_id=new_pidor.user_id,
        chat_id=new_pidor.chat_id,
    )

    if await new_member.is_left():
        await message.reply(_.pidor.pidor_left)
        return

    event: PidorEvent = await PidorEvent.create(
        pidor_id=new_pidor.id, chat_id=new_pidor.chat_id
    )

    await new_pidor.update(latest_time=event.id)
    await member.chat.update(pidor_id=new_pidor.id)

    for phrase in choice(_.pidor.pidor_searching).split("\n"):
        if phrase != "":
            await message.answer(italic(phrase))
        if not ignore_pidor_wait:
            await asyncio.sleep(2.5)

    await message.answer(
        choice(
            _.pidor.today_pidor,
            user=bold(new_member.tag),
        )
    )


PIDOR_TEMPLATE = "_{}_ *{}* — `{}` {}\n"


def get_emojed_num(num: int) -> str:
    return ["🥇", "🥈", "🥉", f"{num}."][min(num - 1, 3)]


@router.message(Command("pidorstats"))
async def pidor_stats(message: types.Message, _: Locale):
    member = await Member.get_by(message)

    msg = _.pidor.top_10 + "\n\n"

    for num, pidor in enumerate(
        await member.get_top_pidors(), 1
    ):
        count = prettyword(pidor.count, _.count)

        msg += PIDOR_TEMPLATE.format(
            get_emojed_num(num),
            pidor.full_name,
            pidor.count,
            count,
        )

    msg += "\n"
    msg += _.pidor.total_members(
        count=await member.get_pidor_count()
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

    if is_created:
        await message.reply(_.pidor.in_db, parse_mode="Markdown")
        return

    await message.reply(_.pidor.already_in_db)
