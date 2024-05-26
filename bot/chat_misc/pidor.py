import asyncio
from time import time

from aiogram import types
from aiogram.utils.markdown import bold, italic

from aiogram.filters import Command
from ..config import bot, router, choice
from ..database import Member, PidorEvent
from ..lib.text import prettyword
from fluentogram import TranslatorRunner


@router.message(Command("pidor"))
async def find_pidor(
    message: types.Message,
    _: TranslatorRunner,
    ignore_pidor_wait: bool = False,
):
    member = await Member.get_by(message)
    await member.fetch_related("chat", "pidor")

    if message.chat.id > 0:
        await message.reply(_.pidor.work_only_in_chats())
        return

    if not await member.chat.can_run_pidor():
        pidor = await Member.get(id=member.chat.pidor_id)
        await pidor.fetch_related("user", "pidor")

        return await message.reply(
            choice(_.pidor.templates.finden, user=bold(pidor.mention))
        )

    if not member.pidor or not member.pidor.is_allowed:
        return await message.reply(_("pidor.reg"), parse_mode="None")

    new_pidor = await member.chat.get_random_pidor()

    if await new_pidor.get_status() == "left":
        await message.reply(_.pidor.pidor_left())
        return

    await new_pidor.fetch_related("pidor", "user")

    event = await PidorEvent.create(
        pidor_id=new_pidor.id, chat_id=new_pidor.chat_id
    )

    await new_pidor.pidor.update(latest_time=event.id)
    await member.chat.update(pidor_id=new_pidor.id)

    for phrase in choice(_.pidor.finding).split("\n")[:-1]:
        if phrase != "":
            await message.answer(italic(phrase))
        if not ignore_pidor_wait:
            await asyncio.sleep(2.5)

    await message.answer(
        choice(_.pidor.templates.finden, user=bold(new_pidor.tag))
    )

    if message.chat.id == -1001176998310:
        try:
            await bot.restrict_chat_member(
                new_pidor.chat.id,
                new_pidor.user.id,
                until_date=time() + 60,
            )
        except Exception:
            pass


PIDOR_TEMPLATE = "_{}_ *{}* — `{}` {}\n"


def get_emojed_num(num: int) -> str:
    match num:
        case 1:
            return "🥇"
        case 2:
            return "🥈"
        case 3:
            return "🥉"

    return num + "."


@router.message(Command("pidorstats"))
async def pidor_stats(message: types.Message, _: TranslatorRunner):
    member = await Member.get_by(message)
    await member.fetch_related("chat")

    msg = _.pidor.top_10() + "\n\n"

    for num, pidor in enumerate(
        await member.chat.get_top_pidors(), 1
    ):
        count = prettyword(pidor.count, _.count())

        msg += PIDOR_TEMPLATE.format(
            get_emojed_num(num), pidor.full_name, pidor.count, count
        )

    msg += "\n"
    msg += _.pidor.members(count=await member.get_pidor_count())

    await message.reply(msg, parse_mode="Markdown")


@router.message(Command("pidorreg", "pidoreg"))
async def reg_pidor(
    message: types.Message,
    _: TranslatorRunner,
):
    member = await Member.get_by(message)
    pidor, is_created = await member.get_pidor()

    if is_created:
        return await message.reply(_.in_db())

    await message.reply(_.already_in_db())
