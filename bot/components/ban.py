from .token import bot
from .texts import texts
from .lib.wikipedia import Wikipedia
from .rules import chat_rules
from .random import random_putin, random_lukash
from .wiki import getWiki

from random import choice, randint
import time
import re


@bot.message_handler(content_types=['text'])
def detect(message):
    if message.text.startswith("/w_"):
        text = message.text.replace("/w_", "")
        if text.find("@") != -1:
            text = text.split("@", maxsplit=1)[0]
        w = Wikipedia("ru")

        try:
            id_ = int(text)

        except Exception as e:
            bot.reply_to(message, "id должен быть числом")
            return

        title = w.getPageNameById(id_)

        if title == -1:
            bot.reply_to(message, "Не получилось найти статью по айди")
            return

        getWiki(message, title=title)

    if message.chat.id == -1001335444502 or \
       message.chat.id == -1001189395000 or \
       message.chat.id == -1001176998310:
        msg = message.text.lower().replace("_", "") \
                                  .replace("-", "")

        for word in texts["love_words"]:
            if word in msg:
                bot.send_sticker(
                    message.chat.id,
                    "CAACAgIAAx0CRieRpgABA7bCX1aW70b_1a0OspsDDXYk8iPACEkAArwBAAKUmWkvXbzmLd8q5dcbBA",
                    reply_to_message_id=message.message_id
                )
                break

        if msg.find("бот, сколько") != -1 and msg.find("?") != -1:
            number = randint(0, 100000)
            randnum = randint(0, 10000000)

            if randnum == 34563:
                bot.reply_to(message, "Столько")

            else:
                word = msg.replace("бот, сколько", "").split()[0]
                bot.reply_to(message, f"{str(number)} {word}")

        elif msg.find("бот, почему") != -1 and msg.find("?") != -1:
            bot.reply_to(message, choice(texts["why_list"]))

        elif msg.find("бот,") != -1 and msg.find("?") != -1:
            bot.reply_to(message, choice(["Да", "Нет"]))

        if msg.find("бойкот") != -1:
            bot.reply_to(message, "Вы запостили информацию о бойкоте, если вы бойкотировали, то к вам приедут с паяльником")

        if msg.find("яблоко") != -1 or \
           msg.find("яблочник") != -1:
            bot.reply_to(message, "Вы запостили информацию о яблоке, если вы яблочник, то к вам приедут с паяльником")

        if re.search(r"(^|[^a-zа-яё\d])[бb][\W]*[аa][\W]*[нn]([^a-zа-яё\d]|$)",
                     message.text
                     .lower()
                     .replace("H", "н")
                     .replace("α", "а")
                     .replace("@", "а")
                     .replace("🅰️", "а")
                     .replace("🅱️", "б")):

            if message.from_user.id in texts["ban_list"]:
                bwords = texts["ban_list"][message.from_user.id]
            else:
                bwords = texts["ban_list"]["all"]

            bword = choice(bwords)

            if type(bword) == str:
                bot.reply_to(message, bword)

            elif type(bword) == dict:
                bot.reply_to(message, bword["text"])
                bot.send_sticker(message.chat.id, bword["sticker"])

            try:
                bot.restrict_chat_member(message.chat.id,
                                         message.from_user.id,
                                         until_date=time.time()+60)
            except:
                pass

        if msg.find("секс") != -1:
            bot.reply_to(message, "Кто?")

        if msg.find("когда уйдет путин") != -1:
            random_putin(message)

        if msg.find("когда уйдет лукашенко") != -1:
            random_lukash(message)


@bot.message_handler(content_types=["new_chat_members"])
def john(message):
    if message.chat.id != -1001319828458 and message.chat.id != -1001189395000:
        bot.reply_to(message, f'{choice(texts["greatings"])}?')

    if message.chat.id == -1001335444502 or message.chat.id == -1001176998310:
        chat_rules(message, False)
