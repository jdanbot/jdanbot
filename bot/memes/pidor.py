import datetime
from time import time
from random import choice
from ..locale import locale
from ..lib.text import prettyword
from ..config import bot, conn, dp, pidors, pidorstats


async def getUserName(chat_id, user_id, enable_tag=False):
    pidorinfo = await bot.get_chat_member(chat_id, user_id)

    try:
        return ("@" if enable_tag else "") + pidorinfo.user.username
    except Exception:
        return pidorinfo.user.first_name


@dp.message_handler(commands=["pidor"])
async def find_pidor(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    is_katzbots = chat_id == -1001176998310
    name = "забаненный" if is_katzbots else "пидор"

    curchat = await pidors.getPidorInfo(chat_id)
    all_pidors = await pidorstats.select(where=f"{chat_id = }")
    user_stats = await pidorstats.select(where=(f"{user_id = }",
                                                f"{chat_id = }"))

    if len(user_stats) < 1:
        await message.reply("Ты не в базе. Зарегайся через /pidorreg")
    else:
        if len(curchat) == 0:
            pidor_of_day = choice([pidor[1] for pidor in all_pidors])
            pidorname = await getUserName(chat_id, pidor_of_day, True)

            await message.reply(choice(locale.pidor_templates).format(
                user=pidorname,
                name=name
            ), parse_mode="HTML")

            period = int(datetime.datetime.now().timestamp())

            await pidors.delete(where=f"{chat_id = }")
            await pidors.insert(chat_id, pidor_of_day, period)

            stats = await pidorstats.select(where=[f"{chat_id = }",
                                                   f"user_id={pidor_of_day}"])

            await pidorstats.delete(where=[f"{chat_id = }",
                                           f"user_id = {pidor_of_day}"])
            count = stats[-1][-1]

            await pidorstats.insert(chat_id, pidor_of_day,
                                    stats[-1][3], count + 1)

            stats = await pidorstats.select(where=[f"{chat_id = }",
                                                   f"user_id={pidor_of_day}"])
            await conn.commit()

            if is_katzbots:
                try:
                    await bot.restrict_chat_member(chat_id, pidor_of_day,
                                                   until_date=time()+60)
                except Exception:
                    pass
        else:
            pidorname = await getUserName(chat_id, curchat[0][1])
            await message.reply(choice(locale.pidor_finded_templates).format(
                name=name,
                user=pidorname
            ), parse_mode="HTML")


@dp.message_handler(commands=["pidorstats"])
async def pidor_stats(message):
    chat_id = message.chat.id
    is_katzbots = chat_id == -1001176998310
    name = "забаненных" if is_katzbots else "пидоров"

    pidorstat = await pidorstats.select(where=f"{chat_id = }")
    pidorstat = sorted(pidorstat, key=lambda pidor: pidor[-1])[::-1][:10]
    msg = f"Топ-10 <b>{name}</b> за все время:\n\n"

    for num, pidor in enumerate(pidorstat):
        name = prettyword(pidor[-1], ["раз", "раза", "раз"])
        msg += f"<i>{num + 1}.</i> "
        msg += f"<b>{pidor[2]}</b> — <code>{pidor[-1]}</code> {name}\n"

    msg += f"\nВсе участников — <code>{len(pidorstat)}</code>"

    await message.reply(msg, parse_mode="HTML")


@dp.message_handler(commands=["pidorme"])
async def pidor_me(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    is_katzbots = chat_id == -1001176998310
    name = "забаненным" if is_katzbots else "пидором"

    pidor = await pidorstats.select(where=[f"{chat_id = }",
                                           f"{user_id = }"])

    fcount = prettyword(pidor[-1][-1], ["раз", "раза", "раз"])
    await message.reply(f"Ты был <b>{name} дня</b> {pidor[-1][-1]} {fcount}",
                        parse_mode="HTML")


@dp.message_handler(commands=["pidorreg"])
async def reg_pidor(message):
    pidor = await pidorstats.select(where=[
        f"chat_id={message.chat.id}",
        f"user_id={message.from_user.id}"
    ])

    if len(pidor) == 0:
        username = await getUserName(message.chat.id, message.from_user.id)
        await pidorstats.insert(message.chat.id, message.from_user.id,
                                username, 0)
        await conn.commit()

        await message.reply("Попался в базу, ищи себя в jdanbot.db")
    else:
        await message.reply("Ты уже в базе")
