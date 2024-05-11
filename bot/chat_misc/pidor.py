import asyncio
from random import choice
from time import time

from aiogram import types
from aiogram.utils.markdown import bold, italic

from aiogram.filters import Command
from ..config import bot, router
from ..database import Member, PidorEvent
from ..database import tables as t
from ..lib.text import prettyword
from fluentogram import TranslatorRunner


@router.message(Command("pidor"))
async def find_pidor(
    message: types.Message,
    _: TranslatorRunner,
    ignore_pidor_wait: bool = False,
):
    print(_.finder)
    member = await Member.get_by(message, pidor=True)

    if message.chat.id > 0:
        await message.reply(_.pidor.work_only_in_chats())
        return

    if not await member.chat.can_run_pidor():
        pidor = await Member.get_by_id(member.chat.pidor)

        return await message.reply(
            _(
                "pidor.already_finded_templates",
                user=bold(pidor.mention),
                went_random=True,
            )
        )

    if not member.pidor or not member.pidor.is_allowed:
        await message.reply(_("pidor.reg"))
        return

    new_pidor = await member.chat.get_random_pidor()

    pidor_info = await bot.get_chat_member(
        new_pidor.chat.id, new_pidor.user.id
    )

    if pidor_info.status == "left":
        await message.reply(_("pidor.pidor_left"))
        return

    event = await PidorEvent.insert(new_pidor, new_pidor.chat)

    await t.Pidor.update(latest_time=event).where(
        t.Pidor.member == new_pidor.id
    )

    await t.Chat.update(pidor=new_pidor.id).where(
        t.Chat.id == new_pidor.chat.id
    )

    for phrase in choice(_("pidor.pidor_finding")).split("\n")[:-1]:
        if phrase != "":
            await message.answer(italic(phrase))
        if not ignore_pidor_wait:
            await asyncio.sleep(2.5)

    await message.answer(
        _("pidor.templates", went_random=True, user=new_pidor.tag),
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


PIDOR_TEMPLATE = "_{}_. *{}* — `{}` {}\n"


@router.message(Command("pidorstats"))
async def pidor_stats(message):
    member = await Member.get_by(message)

    msg = _("pidor.top_10") + "\n\n"

    for num, pidor in enumerate(
        await member.chat.get_top_pidors(), 1
    ):
        count = prettyword(pidor.count, _("cases.count"))

        msg += PIDOR_TEMPLATE.format(
            num, member.user.full_name, pidor.count, count
        )

    msg += "\n"
    msg += _(
        "pidor.members", count=await member.chat.get_pidor_count()
    )

    await message.reply(msg, parse_mode="Markdown")


@router.message(Command("pidorreg"))
async def reg_pidor(message: types.Message):
    member = await Member.get_by(message)
    pidor, status = await member.get_pidor()

    if status:
        return await message.reply(
            _("pidor.in_db"), parse_mode="Markdown"
        )

    await message.reply(
        _("pidor.already_in_db"), parse_mode="Markdown"
    )
