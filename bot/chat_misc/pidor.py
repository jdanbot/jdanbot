from aiogram import types
from aiogram.utils.markdown import escape_md, italic

import asyncio

from datetime import datetime

from peewee import fn, JOIN, SQL

from beanie.operators import Push

from time import time
from random import choice

from ..lib.text import prettyword
from ..config import bot, dp, _
from ..database import engine, Member, Chat, Pidor, PidorEvent

# from ..schemas import ChatMember, Chat, Pidor, PidorEvent


@dp.message_handler(commands=["pidor"])
async def find_pidor(
    message: types.Message, ignore_pidor_wait: bool = False
):
    member = await Member.get_by(message)

    if message.chat.id > 0:
        await message.reply(_("pidor.work_only_in_chats"))
        return

    if False and not member.chat.can_run_pidor_finder:
        pidor_member = await Member.get(
            id=Pidor.get(id=member.chat.pidor.id).member_id
        )

        await message.reply(
            _(
                "pidor.already_finded_templates",
                user=escape_md(pidor_member.mention),
                went_random=True,
            ),
            parse_mode="MarkdownV2",
        )
        return

    if not member.pidor or not member.pidor.is_allowed:
        await message.reply(_("pidor.reg"))
        return

    new_pidor: Member = choice(await member.chat.pidors())
    pidor_info = await bot.get_chat_member(
        new_pidor.chat.tg_id, new_pidor.user.tg_id
    )

    if pidor_info.status == "left":
        await message.reply(_("pidor.pidor_left"))
        return

    chat = await Chat.get_by(message)

    chat.pidor_events.extend([PidorEvent(pidor=new_pidor.pidor)])

    # chat.pidor = new_pidor.id
    await engine.save(chat)

    for phrase in choice(_("pidor.pidor_finding")).split("\n")[:-1]:
        if phrase != "":
            await message.answer(
                italic(phrase), parse_mode="MarkdownV2"
            )
        if not ignore_pidor_wait:
            await asyncio.sleep(2.5)

    await message.answer(
        _("pidor.templates", went_random=True, user=new_pidor.tag),
        parse_mode="MarkdownV2",
    )

    if message.chat.id == -1001176998310:
        try:
            await bot.restrict_chat_member(
                new_pidor.chat.tg_id,
                new_pidor.user.tg_id,
                until_date=time() + 60,
            )
        except Exception:
            pass


PIDOR_TEMPLATE = "_{}_. *{}* — `{}` {}\n"


@dp.message_handler(commands=["pidorstats"])
async def pidor_stats(message):
    top_pidors = (
        Pidor.select(
            Pidor, fn.Count(PidorEvent.id).alias("pidor_count")
        )
        .join(PidorEvent, on=PidorEvent.pidor_id == Pidor.id)
        .join(ChatMember, on=ChatMember.id == Pidor.member_id)
        .join(Chat, on=Chat.id == ChatMember.chat_id)
        .where(Chat.id == message.chat.id)
        .group_by(PidorEvent.pidor_id)
        .order_by(-SQL("pidor_count"))
        .limit(10)
    )

    member_count = (
        Pidor.select()
        .join(ChatMember, on=ChatMember.pidor_id == Pidor.id)
        .join(Chat, on=ChatMember.chat_id == Chat.id)
        .where(Chat.id == message.chat.id)
    ).count()

    msg = _("pidor.top_10") + "\n\n"

    for num, pidor in enumerate(top_pidors, 1):
        count = prettyword(pidor.count, _("cases.count"))

        member = ChatMember.get(id=pidor.member_id)

        try:
            name = member.user.full_name
        except Exception:
            name = "UNKNOWN"

        msg += PIDOR_TEMPLATE.format(num, name, pidor.count, count)

    msg += "\n"
    msg += _("pidor.members", count=member_count)

    await message.reply(msg, parse_mode="Markdown")


@dp.message_handler(commands=["pidorreg"])
async def reg_pidor(message: types.Message):
    member = await Member.get_by(message)
    pidor, status = await member.get_pidor()

    print(pidor)

    if status:
        await message.reply(_("pidor.in_db"), parse_mode="Markdown")
    else:
        await message.reply(
            _("pidor.already_in_db"), parse_mode="Markdown"
        )
