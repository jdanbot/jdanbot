import asyncio
import datetime

from time import time
from random import choice

from ..lib.text import prettyword, italic
from ..config import bot, dp, Pidor, PidorStats, _


async def getUserName(chat_id, user_id, enable_tag=False):
    pidorinfo = await bot.get_chat_member(chat_id, user_id)

    try:
        return ("@" if enable_tag else "") + pidorinfo.user.username
    except Exception:
        return pidorinfo.user.first_name


@dp.message_handler(commands=["pidor"])
async def find_pidor(message):
    chat_id = message.chat.id

    curchat = await Pidor.getPidorInfo(chat_id)
    all_pidors = list(
        PidorStats.select()
                  .where(PidorStats.chat_id == message.chat.id)
    )

    user_stats = list(
        PidorStats.select()
                  .where(PidorStats.chat_id == message.chat.id,
                         PidorStats.user_id == message.from_user.id)
    )

    if message.chat.id > 0:
        await message.reply(_("pidor.work_only_in_chats"))
        return

    if len(user_stats) < 1:
        await message.reply(_("pidor.reg"))
    else:
        if len(curchat) == 0:
            pidor_of_day = choice([pidor.user_id for pidor in all_pidors])
            pidorinfo = await bot.get_chat_member(chat_id, pidor_of_day)

            if pidorinfo.status == "left":
                await message.reply(_("pidor.pidor_left"),
                                    parse_mode="HTML")
                return

            try:
                pidorname = "@" + pidorinfo.user.username
            except Exception:
                pidorname = pidorinfo.user.first_name

            period = int(datetime.datetime.now().timestamp())
            curchat = list(
                Pidor.select()
                     .where(Pidor.chat_id == message.chat.id)
            )

            if len(curchat) > 1:
                (Pidor.update(user_id=pidor_of_day, timestamp=period)
                      .where(Pidor.chat_id == message.chat.id)
                      .execute())
            else:
                Pidor.insert(chat_id=message.chat.id, user_id=pidor_of_day,
                             timestamp=period).execute()

            PidorStats.update(count=PidorStats.count + 1) \
                      .where(PidorStats.chat_id == message.chat.id,
                             PidorStats.user_id == pidor_of_day) \
                      .execute()

            for phrase in choice(_("pidor.pidor_finding")).split("\n")[:-1]:
                await message.answer(italic(phrase), parse_mode="HTML")
                await asyncio.sleep(2.5)

            await message.answer(
                choice(_("pidor.templates", user=pidorname)),
                parse_mode="HTML")

            if message.chat.id == -1001176998310:
                try:
                    await bot.restrict_chat_member(chat_id, pidor_of_day,
                                                   until_date=time()+60)
                except Exception:
                    pass
        else:
            pidorname = await getUserName(chat_id, curchat[0].user_id)
            await message.reply(choice(_("pidor.already_finded_templates",
                                         user=pidorname
                                         )), parse_mode="HTML")


@dp.message_handler(commands=["pidorstats"])
async def pidor_stats(message):
    pidorstat = PidorStats.select() \
                          .where(PidorStats.chat_id == message.chat.id) \
                          .order_by(-PidorStats.count) \
                          .limit(10)

    msg = _("pidor.top_10")
    msg += "\n\n"

    for num, pidor in enumerate(pidorstat):
        count = prettyword(pidor.count, _("cases.count"))
        msg += f"<i>{num + 1}.</i> "
        msg += f"<b>{pidor.username}</b> — <code>{pidor.count}</code> {count}\n"

    msg += "\n"
    msg += _("pidor.members", count=len(pidorstat))

    await message.reply(msg, parse_mode="HTML")


@dp.message_handler(commands=["pidorme"])
async def pidor_me(message):
    pidor = (PidorStats.select()
                       .where(PidorStats.chat_id == message.chat.id,
                              PidorStats.user_id == message.from_user.id)
                       .get())

    await message.reply(_("pidor.me", count=pidor.count,
                          fcount=prettyword(pidor.count, _("cases.count"))),
                        parse_mode="HTML")


@dp.message_handler(commands=["pidorreg"])
async def reg_pidor(message):
    pidor = list(
        PidorStats.select()
                  .where(PidorStats.chat_id == message.chat.id,
                         PidorStats.user_id == message.from_user.id)
    )

    username = await getUserName(message.chat.id, message.from_user.id)

    if len(pidor) == 0:
        PidorStats.insert(chat_id=message.chat.id,
                          user_id=message.from_user.id,
                          username=username, count=0).execute()

        await message.reply(_("pidor.in_db"), parse_mode="Markdown")

    elif pidor[-1].username != username:
        pidor = pidor[-1]

        PidorStats.update(username=username) \
                  .where(PidorStats.user_id == message.from_user.id) \
                  .execute()

        await message.reply(_("pidor.status_fixed"))

    else:
        await message.reply(_("pidor.already_in_db"), parse_mode="Markdown")
