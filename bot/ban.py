from aiogram import types

from .config import dp, bot
from .locale import locale
from .memes.random import random_putin, random_lukash

from .spy import activate_spy
from .lib.text import code

from random import choice, randint
from .notes import getNote

import traceback
import time
import re


@dp.message_handler(commands=["admins"])
async def call_admins(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text="Да", callback_data="call_admin"),
        types.InlineKeyboardButton(text="Удолить", callback_data="delete"))

    await message.reply("Вы точно уверен, что хочешь призвать админов? 🌚",
                        reply_markup=keyboard)


@dp.callback_query_handler(lambda call: call.data == "delete")
async def delete_call(call):
    await call.message.delete()


@dp.callback_query_handler(lambda call: call.data == "call_admin")
async def call_admin(call):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Удолить",
                                            callback_data="delete"))

    admins = await bot.get_chat_administrators(call.message.chat.id)

    true_admins = []

    for admin in admins:
        try:
            if not admin.user.is_bot:
                true_admins.append("@" + admin.user.username)
        except Exception:
            pass

    admins_call = ", ".join(true_admins) + ". "

    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text=admins_call + "Все, вызвал админов, тiкай з чату",
                                reply_markup=keyboard)


@dp.message_handler(content_types=["new_chat_members"])
async def john(message):
    greatings = await getNote(message.chat.id, "__enable_greatings__")
    welcome = await getNote(message.chat.id, "__enable_welcome__")

    greatings = True if greatings == "True" else False
    welcome = True if welcome == "True" else False

    if greatings or welcome:
        await message.reply(f"{choice(locale.greatings)}?")

    if message.from_user.id == 795449748:
        await message.reply(f"{choice(locale.jdan_welcome)}?")

    rules = await getNote(message.chat.id, "__rules__")

    if rules is not None:
        try:
            await message.answer(rules,
                                 parse_mode="MarkdownV2")
        except Exception:
            await message.answer(rules)


@dp.message_handler(content_types=["left_chat_member"])
async def left_john(message):
    if message.chat.id != -1001319828458 and message.chat.id != -1001189395000:
        await message.reply(f'{choice(locale.greatings)} ушел?')


@dp.message_handler(lambda message: True)
async def message_handler(message):
    try:
        await activate_spy(message)
    except Exception:
        print(code(traceback.format_exc()))

    try:
        response = await getNote(message.chat.id, "__enable_response__")
    except TypeError:
        response = "False"

    if response == "True":
        await detect_text_message(message)


async def detect_text_message(message):
    msg = message.text.lower().replace("_", "") \
                              .replace("-", "")

    for word in locale.love_words:
        if word in msg:
            await message.reply_sticker(locale.honka.send_love)
            break

    if msg.find("бот, сколько") != -1 and msg.find("?") != -1:
        number = randint(0, 10000)
        randnum = randint(0, 10000000)

        if randnum == 34563:
            await message.reply("Столько")

        else:
            word = msg.replace("бот, сколько", "").split()[0]
            await message.reply(f"{str(number)} {word}")

    elif msg.find("бот, почему") != -1 and msg.find("?") != -1:
        await message.reply(choice(locale.why_list))

    elif msg.find("бот,") != -1 and msg.find("?") != -1:
        await message.reply(choice(["Да", "Нет"]))

    if msg.find("бойкот") != -1:
        await message.reply(locale.ban.boikot)

    if msg.find("яблоко") != -1 or \
       msg.find("яблочн") != -1:
        await message.reply(locale.ban.apple)

    if re.search(r"(^|[^a-zа-яё\d])[бb][\W]*[аa][\W]*[нnh]([^a-zа-яё\d]|$)",
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

        try:
            bwords = locale.ban_list.__dict__[message.from_user.id]
        except KeyError:
            bwords = locale.ban_list.all

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

    if msg.find("секс") != -1:
        await message.reply("Что?")

    # if msg.find(" наки ") != -1:
    #     await message.reply("Майкл Наки — в жопе козинаки")

    if msg.find("бот,") != -1 and msg.find("когда уйдет путин") != -1:
        await random_putin(message)

    if msg.find("бот,") != -1 and msg.find("когда уйдет лукашенко") != -1:
        await random_lukash(message)
