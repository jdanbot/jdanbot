from .token import bot
from . import texts
from .lib.wikipedia import Wikipedia
from .rules import chat_rules
from .random import random_putin, random_lukash
from .wiki import getWiki

from random import choice, randint
from time import time
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

        if msg.find("бот, сколько") != -1 and msg.find("?") != -1:
            number = randint(0, 100000)
            randnum = randint(0, 10000000)

            if randnum == 34563:
                bot.reply_to(message, "Столько")

            else:
                word = msg.replace("бот, сколько", "").split()[0]
                bot.reply_to(message, f"{str(number)} {word}")

        elif msg.find("бот, спасибо") != -1 or \
             msg.find("бот, ты крутой") != -1 or \
             msg.find("бот, ты молодец") != -1 or \
             msg.find("бот, ты хороший") != -1 or \
             msg.find("бот, ты красавчик") != -1 or \
             msg.find("бот, красавчик") != -1:
            bot.send_sticker(
                message.chat.id,
                "CAACAgIAAx0CRieRpgABA7bCX1aW70b_1a0OspsDDXYk8iPACEkAArwBAAKUmWkvXbzmLd8q5dcbBA",
                reply_to_message_id=message.message_id
            )

        elif msg.find("бот, почему") != -1 and msg.find("?") != -1:
            bot.reply_to(message, choice(["Лень", "Омерика виновата", "Кац ролик не выпустил", "Интернета не было", "Не знаю", "Германия замешана", "Диды ваевали!!!", "Не было денег", "Так исторически сложилось", "Так надо", "Лучше забыть то, о чем тут говорилось", "Не скажу"]))

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
            if message.from_user.id == 332052812:
                bot.reply_to(message, "В ГрОбу я видел эти ваши баны!")

            elif message.from_user.id == 795449748:
                bot.reply_to(message, "Бота фикси! Фикси, фикси, фикси)))")

                bot.send_sticker(
                    message.chat.id,
                    "CAACAgIAAx0CT5lEFgACSRpfRVIg31aW6SvtFAlEo_yvKr_cHAACBAIAApSZaS9-0IPui2d2SBsE"
                )

            elif message.from_user.id == 319384276:
                bot.reply_to(message, "ДИКтаторов не обслуживаю")
                bot.send_sticker(
                    message.chat.id,
                    "CAACAgIAAx0CT5lEFgACSRZfRVIL4Tbw5VUWeOMiwuvnzyzgxAAC3wEAApSZaS95fMgpAr5gbhsE"
                )

            elif message.from_user.id == 340945249:
                bot.reply_to(message,
                             "Теперь админы с <s>народом</s> баном",
                             parse_mode="HTML")

            elif message.from_user.id == 207305797:
                bot.reply_to(message, "Не фальсифицируй бота)))")

            elif message.from_user.id == 388661254:
                bot.reply_to(message, "Ну как там с <s>деньгами</s> фиксом?")

            elif message.from_user.id == 714974074:
                bot.reply_to(message, "Клоун.")

            elif message.from_user.id == 583264555 or message.from_user.id == 1134491227:
                bot.reply_to(message, "Произошел скам...")

            elif message.from_user.id == 197416875:
                bot.reply_to(message, "Где новый стикер?")

            elif message.from_user.id == 1065896779:
                bot.reply_to(message, "Иван, в бан))")

            elif message.from_user.id == 1028275690:
                bot.reply_to(message, "За императрицу!")

            elif message.from_user.id == 619489012:
                bot.reply_to(message, "Ура, председатель пришел))")

            else:
                bot.reply_to(message, choice(texts.ban_list))

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
        bot.reply_to(message, f'{choice(texts.greatings)}?')
    if message.chat.id == -1001335444502 or message.chat.id == -1001176998310:
        chat_rules(message, False)
