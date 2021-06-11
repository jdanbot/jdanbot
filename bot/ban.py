from aiogram import types
from aiogram.types import ContentType

from .config import dp, bot, _, notes
from .memes.random import random_putin, random_lukash, random_navalny

from .lib.text import code
from .lib import handlers

from random import choice, randint

import traceback
import time
import re


@dp.message_handler(commands=["admins"])
@handlers.check("__enable_admin__")
async def call_admins(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(text=_("triggers.yes_"),
                                   callback_data="call_admin"),

        types.InlineKeyboardButton(text=_("triggers.delete"),
                                   callback_data="delete"))

    await message.reply(_("triggers.call_admin_warn"),
                        reply_markup=keyboard)


@dp.callback_query_handler(lambda call: call.data == "delete")
async def delete_call(call):
    await call.message.delete()


@dp.callback_query_handler(lambda call: call.data == "call_admin")
async def call_admin(call):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=_("triggers.delete"),
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
                                text=admins_call + _("triggers.admins_called"),
                                reply_markup=keyboard)


@dp.message_handler(content_types=["new_chat_members"])
async def john(message):
    greatings = await notes.get(message.chat.id, "__enable_greatings__")
    welcome = await notes.get(message.chat.id, "__enable_welcome__")

    if message.from_user.id == 795449748:
        await message.reply(f"{choice(_('triggers.jdan_welcome'))}")

    elif greatings == "True" or welcome == "True":
        await message.reply(f"{choice(_('triggers.welcome'))}?")

    rules = await notes.get(message.chat.id, "__rules__")

    if rules is not None:
        try:
            await message.answer(rules, parse_mode="MarkdownV2")
        except Exception:
            await message.answer(rules)


@dp.message_handler(content_types=["left_chat_member"])
async def left_john(message):
    if message.chat.id != -1001319828458 and message.chat.id != -1001189395000:
        await message.reply(f'{choice(_("triggers.welcome"))} ушел?')


@dp.message_handler()
async def message_handler(message):
    try:
        if message.from_user.id == 675257916 and \
           message.forward_from_chat.id == -1001113237212:
            await message.delete()
            return

    except Exception:
        pass

    try:
        response = await notes.get(message.chat.id, "__enable_response__")
    except TypeError:
        response = "False"

    if response == "True":
        await detect_text_message(message)


async def detect_text_message(message):
    msg = message.text.lower().replace("_", "") \
                              .replace("-", "")

    for word in _("triggers.love_words"):
        if word in msg:
            await message.reply_sticker('CAACAgIAAx0CRieRpgABA7bCX1aW70b_1a0OspsDDXYk8iPACEkAArwBAAKUmWkvXbzmLd8q5dcbBA')
            return

    if msg.find("бот,") != -1 and msg.find("когда уйдет путин") != -1:
        await random_putin(message)
        return

    if msg.find("бот,") != -1 and msg.find("когда уйдет лукашенко") != -1:
        await random_lukash(message)
        return

    if msg.find("бот,") != -1 and msg.find("когда выйдет навальный") != -1:
        await random_navalny(message)
        return

    if msg.find("бот, сколько") != -1 and msg.find("?") != -1:
        number = randint(0, 10000)
        randnum = randint(0, 10000000)

        if randnum == 34563:
            await message.reply("Столько")

        else:
            word = msg.replace("бот, сколько", "").split()[0]
            await message.reply(f"{str(number)} {word}")

    elif msg.find("бот, почему") != -1 and msg.find("?") != -1:
        await message.reply(choice(_("triggers.why_list")))

    elif msg.find("бот,") != -1 and msg.find("?") != -1:
        await message.reply(choice(["Да", "Нет"]))

    if msg.find("бойкот") != -1:
        await message.reply(_("triggers.boikot"))

    if msg.find("яблоко") != -1 or \
       msg.find("яблочн") != -1:
        await message.reply(_("triggers.apple"))

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
            bwords = _("triggers.ban_messages")[message.from_user.id]
        except KeyError:
            bwords = _("triggers.ban_messages")["all"]

        bword = choice(bwords)

        if type(bword) == str:
            await message.reply(bword, parse_mode="HTML",
                                disable_web_page_preview=True)

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


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(message):
    try:
        if message.from_user.id == 675257916 and \
           message.forward_from_chat.id == -1001113237212:
            await message.delete()
            return

    except Exception:
        pass
