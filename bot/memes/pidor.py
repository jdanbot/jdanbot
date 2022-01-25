from aiogram import types

import asyncio

from datetime import datetime

from time import time
from random import choice

from ..lib.text import prettyword, italic
from ..config import bot, dp, Pidor, _
from ..database import ChatMember, Chat, Pidor


@dp.message_handler(commands=["pidor"])
async def find_pidor(message: types.Message):
    member = ChatMember.get_by_message(message)

    if message.chat.id > 0:
        await message.reply(_("pidor.work_only_in_chats"))
        return

    if not member.chat.can_run_pidor_finder:
        pidor_member = ChatMember.get(id=Pidor.get(id=member.chat.pidor.id).member_id)

        await message.reply(choice(_("pidor.already_finded_templates",
            user=pidor_member.mention)), parse_mode="HTML")
        return

    if not member.pidor or not member.pidor.is_pidor_allowed:
        await message.reply(_("pidor.reg"))
        return

    new_pidor = ChatMember.get(choice(member.chat.all_pidors).member_id)

    Pidor.update(
        pidor_count=Pidor.pidor_count + 1,
        when_pidor_of_day=datetime.now()
    ).where(Pidor.member_id == new_pidor.id).execute()
    
    Chat.update(pidor=new_pidor.pidor.id).where(Chat.id == new_pidor.chat.id).execute()

    pidor_info = await bot.get_chat_member(new_pidor.chat.id, new_pidor.user.id)

    if pidor_info.status == "left":
        await message.reply(_("pidor.pidor_left"),
                            parse_mode="HTML")
        return

    for phrase in choice(_("pidor.pidor_finding")).split("\n")[:-1]:
        await message.answer(italic(phrase), parse_mode="HTML")
        await asyncio.sleep(2.5)

    await message.answer(choice(_("pidor.templates", user=new_pidor.tag)), parse_mode="HTML")

    if message.chat.id == -1001176998310:
        try:
            await bot.restrict_chat_member(new_pidor.chat.id, new_pidor.user.id,
                                           until_date=time()+60)
        except Exception:
            pass



PIDOR_TEMPLATE = "<i>{}</i>. <b>{}</b> — <code>{}</code> {}\n"


@dp.message_handler(commands=["pidorstats"])
async def pidor_stats(message):
    top_pidors = (
        Pidor.select()
             .join(ChatMember, on=ChatMember.pidor_id == Pidor.id)
             .join(Chat, on=ChatMember.chat_id == Chat.id)
             .where(Chat.id == message.chat.id)
             .order_by(-Pidor.pidor_count)
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
        count = prettyword(pidor.pidor_count, _("cases.count"))

        member = ChatMember.get(id=pidor.member_id)
        msg += PIDOR_TEMPLATE.format(num, member.user.full_name, pidor.pidor_count, count)

    msg += "\n"
    msg += _("pidor.members", count=member_count)

    await message.reply(msg, parse_mode="HTML")


@dp.message_handler(commands=["pidorme"])
async def pidor_me(message):
    member = ChatMember.get_by_message(message)

    await message.reply(_("pidor.me", count=member.pidor.pidor_count,
                          fcount=prettyword(member.pidor.pidor_count, _("cases.count"))),
                        parse_mode="HTML")


@dp.message_handler(commands=["pidorreg"])
async def reg_pidor(message: types.Message):
    member = ChatMember.get_by_message(message)
    pidor, status = member.get_or_create_pidor()

    if status:
        await message.reply(_("pidor.in_db"), parse_mode="Markdown")
    else:
        await message.reply(_("pidor.already_in_db"), parse_mode="Markdown")
