from .bot import dp, bot
from .data import data
from .rules import chat_rules
from .random import random_putin, random_lukash

from random import choice, randint

import time
import re


@dp.message_handler(content_types=["new_chat_members"])
async def john(message):
    if message.chat.id != -1001319828458 and message.chat.id != -1001189395000:
        await message.reply(f'{choice(data["greatings"])}?')

    if message.chat.id == -1001335444502 or message.chat.id == -1001176998310:
        await chat_rules(message, False)


@dp.message_handler(content_types=["left_chat_member"])
async def left_john(message):
    if message.chat.id != -1001319828458 and message.chat.id != -1001189395000:
        await message.reply(f'{choice(data["greatings"])} ушел?')


@dp.message_handler(lambda message: False or
                    message.chat.id == -1001335444502 or
                    message.chat.id == -1001189395000 or
                    message.chat.id == -1001176998310 or
                    message.chat.id == -1001374137898)
async def detect_text_message(message):

    msg = message.text.lower().replace("_", "") \
                              .replace("-", "")

    for word in data["love_words"]:
        if word in msg:
            await message.reply_sticker(data["honka"]["send_love"])
            break

    if msg.find("бот, сколько") != -1 and msg.find("?") != -1:
        number = randint(0, 100000)
        randnum = randint(0, 10000000)

        if randnum == 34563:
            await message.reply("Столько")

        else:
            word = msg.replace("бот, сколько", "").split()[0]
            await message.reply(f"{str(number)} {word}")

    elif msg.find("бот, почему") != -1 and msg.find("?") != -1:
        await message.reply(choice(data["why_list"]))

    elif msg.find("бот,") != -1 and msg.find("?") != -1:
        await message.reply(choice(["Да", "Нет"]))

    # if msg.find("бойкот") != -1:
    #     await message.reply(data["ban"]["boikot"])

    # if msg.find("яблоко") != -1 or \
    #    msg.find("яблочн") != -1:
    #     await message.reply(data["ban"]["apple"])

    if re.search(r"(^|[^a-zа-яё\d])[бb][\W]*[аa][\W]*[нn]([^a-zа-яё\d]|$)",
                 message.text
                        .lower()
                        .replace("H", "н")
                        .replace("α", "а")
                        .replace("@", "а")
                        .replace("🅰️", "а")
                        .replace("🅱️", "б")):

        if message.from_user.id == 1248462292:
            await message.reply("Никакого бана мышам!")
            return

        if message.from_user.id in data["ban_list"]:
            bwords = data["ban_list"][message.from_user.id]
        else:
            bwords = data["ban_list"]["all"]

        bword = choice(bwords)

        if type(bword) == str:
            await message.reply(bword, parse_mode="HTML")

        elif type(bword) == dict:
            await message.reply(bword["text"], parse_mode="HTML")
            await bot.send_sticker(message.chat.id, bword["sticker"])

        try:
            await bot.restrict_chat_member(message.chat.id,
                                           message.from_user.id,
                                           until_date=time.time()+60)
        except Exception:
            pass

    # if msg.find("секс") != -1:
    #     await message.reply("Что?")

    # if msg.find(" наки ") != -1:
    #     await message.reply("Майкл Наки — в жопе козинаки")

    # if msg.find("когда уйдет путин") != -1:
    #     await random_putin(message)

    # if msg.find("когда уйдет лукашенко") != -1:
    #     await random_lukash(message)
