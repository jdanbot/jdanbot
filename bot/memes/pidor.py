import asyncio
import datetime
from time import time
from random import choice
from ..lib.text import prettyword, italic
from ..config import bot, conn, dp, pidors, pidorstats, _


async def getUserName(chat_id, user_id, enable_tag=False):
    pidorinfo = await bot.get_chat_member(chat_id, user_id)

    try:
        return ("@" if enable_tag else "") + pidorinfo.user.username
    except Exception:
        return pidorinfo.user.first_name


@dp.message_handler(commands=["pidor"])
async def find_pidor(message, locale):
    user_id = message.from_user.id
    chat_id = message.chat.id

    curchat = await pidors.getPidorInfo(chat_id)
    all_pidors = await pidorstats.select(where=f"{chat_id = }")
    user_stats = await pidorstats.select(where=(f"{user_id = }",
                                                f"{chat_id = }"))

    if message.chat.id > 0:
        await message.reply(_("pidor.work_only_in_chats"))
        return

    if len(user_stats) < 1:
        await message.reply(_("pidor.reg"))
    else:
        if len(curchat) == 0:
            pidor_of_day = choice([pidor[1] for pidor in all_pidors])
            pidorname = await getUserName(chat_id, pidor_of_day, True)

            period = int(datetime.datetime.now().timestamp())
            curchat = await pidors.select(where=f"{chat_id}")

            if len(curchat) > 1:
                await pidors.delete(where=f"{chat_id = }")
                await pidors.insert(chat_id, pidor_of_day, period)
            else:
                await pidors.insert(chat_id, pidor_of_day, period)

            stats = await pidorstats.select(where=[f"{chat_id = }",
                                                   f"user_id={pidor_of_day}"])

            await pidorstats.update(where=[f"{chat_id = }",
                                           f"user_id={pidor_of_day}"],
                                    count=stats[-1][-1] + 1)
            await conn.commit()

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
            pidorname = await getUserName(chat_id, curchat[0][1])
            await message.reply(choice(_("pidor.already_finded_templates",
                                    user=pidorname
                                )), parse_mode="HTML")


@dp.message_handler(commands=["pidorstats"])
async def pidor_stats(message, locale):
    chat_id = message.chat.id

    pidorstat = await pidorstats.select(where=f"{chat_id = }")
    pidorstat = sorted(pidorstat, key=lambda pidor: pidor[-1])[::-1][:10]

    msg = _("pidor.top_10")
    msg += "\n\n"

    for num, pidor in enumerate(pidorstat):
        count = prettyword(pidor[-1], _("cases.count"))
        msg += f"<i>{num + 1}.</i> "
        msg += f"<b>{pidor[2]}</b> — <code>{pidor[-1]}</code> {count}\n"

    msg += "\n"
    msg += _("pidor.members", count=len(pidorstat))

    await message.reply(msg, parse_mode="HTML")


@dp.message_handler(commands=["pidorme"])
async def pidor_me(message, locale):
    chat_id = message.chat.id
    user_id = message.from_user.id

    pidor = await pidorstats.select(where=[f"{chat_id = }",
                                           f"{user_id = }"])

    count = pidor[-1][-1] if len(pidor) > 0 else 0
    await message.reply(_("pidor.me", count=count,
                          fcount=prettyword(count, _("cases.count"))),
                        parse_mode="HTML")


@dp.message_handler(commands=["pidorreg"])
async def reg_pidor(message, locale):
    chat_id = message.chat.id
    user_id = message.from_user.id

    pidor = await pidorstats.select(where=[f"{chat_id = }", f"{user_id = }"])
    username = await getUserName(message.chat.id, message.from_user.id)

    if len(pidor) == 0:
        await pidorstats.insert(message.chat.id, message.from_user.id,
                                username, 0)
        await conn.commit()

        await message.reply(_("pidor.in_db"),
                              parse_mode="Markdown")

    elif pidor[-1][2] != username:
        pidor = pidor[-1]

        await pidorstats.update(where=[f"{chat_id = }", f"{user_id = }"],
                                username=username)
        await conn.commit()

        await message.reply(_("pidor.name_fixed"))

    else:
        await message.reply(_("pidor.already_in_db"),
                              parse_mode="Markdown")
