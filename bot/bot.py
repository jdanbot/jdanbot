# -- coding: utf8 --

import json
import yaml
import re
import hashlib
import requests
import math
import os
import traceback
import urllib
import time
import sys
from random import choice, randint
from datetime import datetime

import telebot
from art import text2art
from bs4 import BeautifulSoup

import data as texts
from prettyword import prettyword
from rules import getRules

from lib.wikipedia import Wikipedia
from lib.habr import Habr
from lib.photo import Photo
from lib.telegram import Telegram


if "TOKEN" in os.environ:
    bot = telebot.TeleBot(os.environ["TOKEN"])
    heroku = True

else:
    with open("../token2.json") as token:
        heroku = False
        bot = telebot.TeleBot(json.loads(token.read())["token"])

separator = "/" if os.name == "posix" or os.name == "macos" else "\\"
start_time = datetime.now()


keyboard = telebot.types.InlineKeyboardMarkup()

buttons = [
    ["Главная", "main"],
    ["Математика", "math"],
    ["Онлайн-ресурсы", "network"],
    ["Работа с текстом", "text"],
    ["Работа с изображениями", "images"],
    ["Служебные команды", "commands"],
    ["Шифровая херня", "crypt"],
    ["Мемы", "memes"]
]

for ind, button in enumerate(buttons):
    buttons[ind] = telebot.types.InlineKeyboardButton(text=button[0], callback_data=button[1])

for ind, button in enumerate(buttons):
    a = buttons[ind:ind + 2]
    try:
        buttons.remove(a[1])
    except:
        pass
    keyboard.add(*a)


def fixHTML(code):
    return code.replace("<", "&lt;").replace(">", "&gt;")


@bot.message_handler(["habr"])
def habr(message):
    options = message.text.split(maxsplit=1)
    if len(options) == 1:
        bot.reply_to(message, "Введи id поста из хабра")
        return

    try:
        id_ = int(options[-1])

    except:
        bot.reply_to(message, "Введи валидный id поста")

    h = Habr()
    try:
        bot.reply_to(message, h.page(id_)[:4096], parse_mode="HTML", disable_web_page_preview=True)
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(["art"])
def art(message):
    options = message.text.split(maxsplit=1)
    if len(options) == 1:
        bot.reply_to(message, "Введи текст на английском для получения арта")
        return

    try:
        if len(options[1]) > 20:
            bot.reply_to(message, "Ты шизик.")
            return

        art = text2art(options[1], chr_ignore=True).replace("<", "&lt;") \
                                                   .replace(">", "&gt;")
        bot.reply_to(message,
                     f"<code>{art}</code>",
                     parse_mode="HTML")
    except:
        bot.reply_to(message, "Не получилось сделать арт")


@bot.message_handler(["new_menu", "start", "help"])
def menu(message):
    bot.reply_to(message, texts.main, parse_mode="HTML", reply_markup=keyboard)


def edit(call, text):
    try:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=text,
                              parse_mode="HTML",
                              reply_markup=keyboard)
    except Exception as e:
        bot.answer_callback_query(callback_query_id=call.id,
                                  text="Вы уже в этом пункте")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "main":
        edit(call, texts.main)

    if call.data == "math":
        edit(call, texts.math)

    if call.data == "text":
        edit(call, texts.text)

    if call.data == "network":
        edit(call, texts.network)

    if call.data == "math":
        edit(call, texts.math)

    if call.data == "images":
        edit(call, texts.images)

    if call.data == "commands":
        edit(call, texts.commands)

    if call.data == "crypt":
        edit(call, texts.crypt)

    if call.data == "memes":
        edit(call, texts.memes)


# @bot.message_handler(content_types=["text"])
# def abc(message):
#     if message.text.find("/") != -1:
#         getWiki(message, "en", abc=message.text.replace("/", ""))


@bot.message_handler(["e"])
def supereval(message):
    if message.from_user.id == 795449748:
        command = message.text.split(maxsplit=1)[1]
        try:
            output = str(eval(command)).replace("<", "&lt;") \
                                       .replace(">", "&gt;")
        except:
            output = str(traceback.format_exc()).replace("<", "&lt;") \
                                                .replace(">", "&gt;")

        bot.reply_to(message,
                     f"<code>{str(output)}</code>",
                     parse_mode="HTML")


@bot.message_handler(commands=["rules"])
def chat_rules(message, reply=True):
    rules = getRules("Ustav-profsoyuza-Botov-Maksima-Kaca-08-15")
    bot.send_chat_action(message.chat.id, "typing")
    if reply:
        bot.reply_to(message,
                     f'<b>{rules["title"]}</b>\n\n{rules["description"]}',
                     parse_mode="HTML")
    else:
        bot.send_message(message.chat.id,
                         f'<b>{rules["title"]}</b>\n\n{rules["description"]}',
                         parse_mode="HTML")


@bot.message_handler(["uptime"])
def get_uptime(message):
    uptime = str(datetime.now() - start_time)
    main = uptime.split(".")[0].split(":")

    text = f"uptime:\n"
    text += f"├─hours: {main[0]}\n"
    text += f"├─minutes: {main[1]}\n"
    text += f"└─seconds: {main[2]}\n"

    bot.reply_to(message,
                 f"`{text}`",
                 parse_mode="Markdown")


@bot.message_handler(["status"])
def status(message):

    uptime = str(datetime.now() - start_time)
    main = uptime.split(".")[0].split(":")

    text =  f"bot:\n"
    text += f"├─status: working\n"
    text += f"├─uptime:\n"
    text += f"│⠀├─hours: {main[0]}\n"
    text += f"│⠀├─minutes: {main[1]}\n"
    text += f"│⠀└─seconds: {main[2]}\n"
    text += f"├─heroku: {heroku}\n"
    text += f"└─osname: {os.name}\n"

    text = text.replace("False", "❌") \
               .replace("True", "✅")

    bot.reply_to(message,
                 f"`{text}`",
                 parse_mode="Markdown")


@bot.message_handler(["to_yaml"])
def toyaml(message):
    if message.reply_to_message:
        code = message.reply_to_message.text
        try:
            j = json.loads(code)
            y = yaml.dump(j, allow_unicode=True)[:4096]
            bot.reply_to(message,
                         f"<code>{fixHTML(y)}</code>",
                         parse_mode="HTML")
        except:
            bot.reply_to(message, "Произошла ошибка при перекодировании")
    else:
        bot.reply_to(message, "Ответь на json")
        return


@bot.message_handler(["title"])
def title(message):
    if len(message.text.split(maxsplit=1)) == 2:
        text = message.text.split(maxsplit=1)[1]

    elif hasattr(message.reply_to_message, "text"):
        text = message.reply_to_message.text

    else:
        bot.reply_to(message, "Ответь на сообщение")
        return

    bot.reply_to(message, text.title())


@bot.message_handler(["d"])
def download(message):
    if not message.from_user.id == 795449748:
        return

    options = message.text.split(maxsplit=1)

    if len(options) == 1:
        bot.reply_to(message, "Напиши ссылку")
        return

    try:
        try:
            r = requests.get(options[1])

        except requests.exceptions.MissingSchema:
            r = requests.get(f"https://{options[1]}")

        bot.reply_to(message,
                     f'<code>{fixHTML(r.text)[:4096]}</code>',
                     parse_mode="HTML")

    except Exception as e:
        bot.reply_to(message,
                     f'<code>Ошибка, тебе бан))))</code>',
                     parse_mode="HTML")


@bot.message_handler(["wget", "r", "request"])
def wget(message):
    if len(message.text.split(maxsplit=1)) == 1:
        bot.reply_to(message, "Напиши ссылку")
        return

    time = datetime.now()
    url = message.text.split(maxsplit=1)[1]

    blacklist = ["mb", ".zip", ".7", ".dev", ".gz", "98.145.185.175", ".avi", "movie", "release",".dll", "localhost", ".bin", "0.0.0.1", "repack", "download"]

    if url.find("?") != -1: 
        if url.split("/")[-1][:url.find("?")].find(".") != -1:
            bot.reply_to(message, "Бан")
            return

    for word in blacklist:
        if url.lower().find(word) != -1:
            bot.reply_to(message, "Ваша ссылка в черном списке")
            return

    try:
        r = requests.get(url)
    except requests.exceptions.MissingSchema:
        try:
            r = requests.get(f"https://{url}")

        except Exception as e:
            bot.reply_to(message, f"`{str(e)}`", parse_mode="Markdown")
            return
    except Exception as e:
        bot.reply_to(message, f"`{str(e)}`", parse_mode="Markdown")
        return

    load_time = datetime.now() - time

    main = str(load_time).split(".")[0].split(":")

    text = f"{url}\n"

    text += f"├─status_code: {r.status_code}\n"
    text += f"├─size:\n"
    text += f"│⠀├─bytes: {sys.getsizeof(r.text)}\n"
    text += f"│⠀└─megabytes: {str(sys.getsizeof(r.text) * (10**-6))}\n"
    text += f"└─time: {main[1]}:{main[2]}"

    bot.reply_to(message, f"`{text}`", parse_mode="Markdown")


@bot.message_handler(["upper"])
def upper(message):
    if len(message.text.split(maxsplit=1)) == 2:
        text = message.text.split(maxsplit=1)[1]

    elif hasattr(message.reply_to_message, "text"):
        text = message.reply_to_message.text

    else:
        bot.reply_to(message, "Ответь на сообщение")
        return

    bot.reply_to(message, text.upper())


@bot.message_handler(["lower"])
def lower(message):
    if len(message.text.split(maxsplit=1)) == 2:
        text = message.text.split(maxsplit=1)[1]

    elif hasattr(message.reply_to_message, "text"):
        text = message.reply_to_message.text

    else:
        bot.reply_to(message, "Ответь на сообщение")
        return

    bot.reply_to(message, text.lower())


@bot.message_handler(["title"])
def title(message):
    if len(message.text.split(maxsplit=1)) == 2:
        text = message.text.split(maxsplit=1)[1]

    elif hasattr(message.reply_to_message, "text"):
        text = message.reply_to_message.text

    else:
        bot.reply_to(message, "Ответь на сообщение")
        return

    bot.reply_to(message, len(text))


@bot.message_handler(["markdown"])
def md(message):
    if len(message.text.split(maxsplit=1)) == 2:
        text = message.text.split(maxsplit=1)[1]

    elif hasattr(message.reply_to_message, "text"):
        text = message.reply_to_message.text

    else:
        bot.reply_to(message, "Ответь на сообщение")
        return

    bot.reply_to(message, text.title())

    try:
        bot.reply_to(message, text, parse_mode="Markdown")

    except:
        bot.reply_to(message, "Невалидный markdown")


@bot.message_handler(["if"])
def if_(message):
    options = message.text.split()

    if len(options) < 3:
        bot.reply_to(message, "Напиши аргументы :/")

    else:
        result = options[1] == options[2]
        t = "<code>"     # open code tag
        tc = "</code>"   # close code tag

        bot.reply_to(message,
                     f"{t}{options[1]} == {options[2]}{tc}: <b>{result}</b>",
                     parse_mode="HTML")


# @bot.message_handler(["youtube"])
# def downloadYoutube(message):
#     try:
#         message.reply_to_message.text.replace(" ", "").replace(";", "")
#         print("Text")
#     except:
#         bot.reply_to(message, "Ответь на сообщение с ссылкой")
#         return

#     src = f"{os.path.dirname(os.path.abspath(__file__))}{separator}"

#     with youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s', "format": "18"}) as ydl:
#         video = ydl.download([message.reply_to_message.text])
#     print(src + "M1a2JBhacz8.mp4")
#     bot.send_video(message.chat.id, open(src + "M1a2JBhacz8.mp4" , "rb"))


@bot.message_handler(commands=["preview"])
def preview(message):
    try:
        try:
            bot.send_chat_action(message.chat.id, "upload_photo")

            bot.send_photo(message.chat.id, f"https://img.youtube.com/vi/{message.reply_to_message.text.replace('&feature=share', '').split('/')[-1]}/maxresdefault.jpg")
        except:
            bot.send_chat_action(message.chat.id, "upload_photo")

            bot.send_photo(message.chat.id,
                           f'https://img.youtube.com/vi/{urllib.parse.parse_qs(urllib.parse.urlparse(message.reply_to_message.text).query)["v"][0]}/maxresdefault.jpg')
    except Exception as e:
        print(e)
        bot.reply_to(message, "Не получилось скачать превью")


@bot.message_handler(commands=["resize"])
def resize(message):
    tg = Telegram(bot)

    params = tg.parse(message, 3)

    if params == 404:
        bot.reply_to(message,
                     "Недостаточное количество параметров: необходимо `3`",
                     parse_mode="Markdown")
        return

    print(params)
    photo = tg.photo(message)
    file = bot.download_file(photo[1].file_path)

    with open(photo[0] + ".jpg", "wb") as new_file:
        new_file.write(file)

    img = Photo(photo[0] + ".jpg")

    try:
        img.resize([int(params[1]), int(params[2])])
    except Exception as e:
        bot.reply_to(message,
                     f"Произошла ошибка\n<code>{e}</code>",
                     parse_mode="HTML")
        return

    bot.send_photo(message.chat.id, img.save())
    img.clean()


@bot.message_handler(commands=["text"])
def text(message):
    tg = Telegram(bot)

    params = message.text.split(" ", maxsplit=4)

    if len(params) != 5:
        bot.reply_to(message,
                     "Недостаточное количество параметров: необходимо `5`",
                     parse_mode="Markdown")
        return

    print(params)
    photo = tg.photo(message)
    file = bot.download_file(photo[1].file_path)

    with open(photo[0] + ".jpg", "wb") as new_file:
        new_file.write(file)

    img = Photo(photo[0] + ".jpg")
    try:
        img.font("OpenSans-Bold.ttf" if heroku else "../OpenSans-Bold.ttf", int(params[1]))
        img.text(params[2], img.parseXY(params[3]), params[4])
    except Exception as e:
        bot.reply_to(message,
                     f"Произошла ошибка\n<code>{e}</code>",
                     parse_mode="HTML")
        return

    bot.send_photo(message.chat.id, img.save())
    img.clean()


@bot.message_handler(commands=["t"])
def t(message):
    tg = Telegram(bot)

    params = message.text.split(" ", maxsplit=1)

    if len(params) == 1:
        bot.reply_to(message,
                     "Недостаточное количество параметров: необходимо `2`",
                     parse_mode="Markdown")
        return

    print(params)
    photo = tg.photo(message)
    file = bot.download_file(photo[1].file_path)

    with open(photo[0] + ".jpg", "wb") as new_file:
        new_file.write(file)

    img = Photo(photo[0] + ".jpg")
    try:
        img.font("OpenSans-Bold.ttf" if heroku else "../OpenSans-Bold.ttf", 75)
        img.text("black", (50, 50), params[1])
    except Exception as e:
        bot.reply_to(message,
                     f"Произошла ошибка\n<code>{e}</code>",
                     parse_mode="HTML")
        return

    bot.send_photo(message.chat.id, img.save())
    img.clean()


@bot.message_handler(commands=["rectangle"])
def rectangle(message):
    tg = Telegram(bot)

    params = tg.parse(message, 4)

    if params == 404:
        bot.reply_to(message,
                     "Недостаточное количество параметров: необходимо `4`",
                     parse_mode="Markdown")
        return

    print(params)
    photo = tg.photo(message)
    file = bot.download_file(photo[1].file_path)

    with open(photo[0] + ".jpg", "wb") as new_file:
        new_file.write(file)

    img = Photo(photo[0] + ".jpg")

    try:
        img.rectangle(img.parseXY(params[2]), img.parseXY(params[3]), params[1])
    except Exception as e:
        bot.reply_to(message,
                     f"Во время создания фото произошла ошибка\n<code>{e}</code>",
                     parse_mode="HTML")
        return

    bot.send_photo(message.chat.id, img.save())
    img.clean()


@bot.message_handler(commands=["sqrt"])
def sqrt(message):
    try:
        num = float(message.text.split()[1])
        res = math.sqrt(num)

        try:
            res = float(res)

        except:
            res = int(res)

        bot.reply_to(message, f"`{res}`", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"`{e}`", parse_mode="Markdown")


@bot.message_handler(commands=["eval", "calc"])
def calc_eval(message):
    if len(str(message.text).split(maxsplit=1)) == 1:
        bot.reply_to(message, "Введи запрос для вычисления")
        return

    op = message.text.split(maxsplit=1)[1].replace(" ", "") \
                                          .replace("pi", str(math.pi)) \
                                          .replace("e", str(math.e))

    if re.search(r"[а-яА-ЯёЁa-zA-Z]", op):
        bot.reply_to(message, "Необходимая переменная не найдена")
        return

    try:
        result = eval(op)

        if int(result) == float(result):
            text = int(result)
        else:
            text = float(result)

    except ZeroDivisionError:
        text = "Деление на ноль"

    except Exception as e:
        text = f"Некорректный запрос\n{e}"

    bot.reply_to(message, f"`{str(text)}`", parse_mode="Markdown")


@bot.message_handler(["Math"])
def math_command(message):
    pass

# TODO: REWRITE


@bot.message_handler(commands=["sru", "s", "search"])
def wikiru(message):
    wikiSearch(message, "ru")


@bot.message_handler(commands=["wikiru", "wikiru2", "wru", "w"])
def wikiru(message):
    getWiki(message, "ru")


@bot.message_handler(commands=["wikien", "van", "wen", "v"])
def wikien(message):
    getWiki(message, "en")


@bot.message_handler(commands=["wikisv", "wsv"])
def wikisv(message):
    getWiki(message, "sv")


@bot.message_handler(commands=["wikide", "wde"])
def wikide(message):
    getWiki(message, "de")


@bot.message_handler(commands=["wikice", "wce"])
def wikice(message):
    getWiki(message, "ce")


@bot.message_handler(commands=["wikitt", "wtt"])
def wikitt(message):
    getWiki(message, "tt")


@bot.message_handler(commands=["wikiba", "wba"])
def wikiba(message):
    getWiki(message, "ba")


@bot.message_handler(commands=["wikipl", "wpl"])
def wikipl(message):
    getWiki(message, "pl")


@bot.message_handler(commands=["wikiua", "wikiuk", "wuk", "wua", "pawuk"])
def wikiua(message):
    getWiki(message, "uk")


@bot.message_handler(commands=["wikibe",
                               "wbe",
                               "tarakanwiki",
                               "lukaswiki",
                               "potato",
                               "potatowiki"])
def wikibe(message):
    getWiki(message, "be")


@bot.message_handler(commands=["wikies", "wes"])
def wikies(message):
    getWiki(message, "es")


@bot.message_handler(commands=["wikihe", "whe"])
def wikihe(message):
    getWiki(message, "he")


@bot.message_handler(commands=["wikixh", "wxh"])
def wikixh(message):
    getWiki(message, "xh")


@bot.message_handler(commands=["wikiab", "wab"])
def wikiab(message):
    getWiki(message, "ab")


@bot.message_handler(commands=["wikibe-tarask", "wikibet", "wbet", "xbet"])
def wikibet(message):
    getWiki(message, "be-tarask")


@bot.message_handler(commands=["wiki_usage", "wiki2", "wiki"])
def wiki_usage(message):
    bot.reply_to(message, texts.langs, parse_mode="Markdown")


@bot.message_handler(commands=["langs", "wikilangs", "wiki_langs"])
def wiki_langs(message):
    bot.reply_to(message,
                 texts.langs_list,
                 parse_mode="Markdown",
                 disable_web_page_preview=True)


def wikiSearch(message, lang="ru", logs=False):
    if len(message.text.split(maxsplit=1)) != 2:
        bot.reply_to(message, f"Пожалуйста, напишите название статьи\nНапример так: `{message.text.split(maxsplit=1)[0]} Название Статьи`", parse_mode="Markdown")
        return

    query = message.text.split(maxsplit=1)[1]
    print(f"[Wikipedia Search {lang.upper()}] {query}")

    wiki = Wikipedia(lang)

    r = wiki.search(query, 20)

    if r == -1:
        bot.reply_to(message, "Ничего не найдено")
        return

    text = ""

    for prop in r:
        text += f"{prop[0]}\n"
        text += f"└─/w_{prop[1]}\n"

    bot.reply_to(message, text)


def getWiki(message=None, lang="ru", logs=False, title=None):
    wiki = Wikipedia(lang)

    if title is None:
        if len(message.text.split(maxsplit=1)) != 2:
            bot.reply_to(message, f"Пожалуйста, напишите название статьи\nНапример так: `{message.text.split(maxsplit=1)[0]} Название Статьи`", parse_mode="Markdown")
            return

        query = message.text.split(maxsplit=1)[1]
        print(f"[Wikipedia {lang.upper()}] {query}")

        s = wiki.search(query, 1)

        if s == -1:
            bot.reply_to(message, "Ничего не найдено")
            return

        title = s[0][0]

    page = wiki.getPage(title)

    if page == -1:
        text = ""

    elif str(page) == "":
        text = ""

    else:
        for span in page.find_all("span"):
            span.name = "p"

        for p in page.find_all("p"):
            if p.text == "":
                p.replace_with("")

        text = wiki.parsePage(page)

    image = wiki.getImageByPageName(title)

    if type(image) is int:
        bot.send_chat_action(message.chat.id, "typing")
        try:
            bot.reply_to(message, text, parse_mode="HTML")

        except:
            bot.send_message(795449748, text)
            bot.reply_to(message, "Не удалось отправить статью")

    else:
        if image == "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Flag_of_Belarus.svg/1000px-Flag_of_Belarus.svg.png":
            image = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Flag_of_Belarus_%281918%2C_1991%E2%80%931995%29.svg/1000px-Flag_of_Belarus_%281918%2C_1991%E2%80%931995%29.svg.png"

        bot.send_chat_action(message.chat.id, "upload_photo")
        try:
            bot.send_photo(message.chat.id,
                           image,
                           caption=text,
                           parse_mode="HTML",
                           reply_to_message_id=message.message_id)
        except:
            bot.reply_to(message, "Не удалось отправить статью")


@bot.message_handler(commands=["github"])
def github(message):
    try:
        url = message.text.split(maxsplit=1)[1]

    except:
        bot.reply_to(message, "Введи название аккаунта")
        return

    try:
        r = requests.get(f"https://api.github.com/users/{url}")
        repos = requests.get(f"https://api.github.com/users/{url}/repos")
        data = json.loads(r.text)
        repos_list = json.loads(repos.text)
        text = f'*{data["name"]}*\nFollowers `{data["followers"]}` Following `{data["following"]}`\n\n__{data["bio"]}__\n\nRepositories:'

        for repo in repos_list:
            print(repo["full_name"])
            text += f'\n[{repo["full_name"]}]({repo["html_url"]})'

        bot.send_photo(message.chat.id,
                       data["avatar_url"],
                       caption=text,
                       parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, e)


def getImageInfo(url, filename):
    r = requests.get(url + "index.php",
                     params={
                         "search": f"Файл:{filename}"
                     })

    soup = BeautifulSoup(r.text, 'lxml')

    return "https:" + soup.find("div", id="file").a.img["src"]


@bot.message_handler(commands=["lurk"])
def lurk(message, logs=False):
    try:
        name = message.text.split(maxsplit=1)[1]
    except:
        bot.reply_to(message, "Введите название статьи")
        return

    if logs:
        print(f"[TEST] [Lurkmore] {name}")
    else:
        print(f"[Lurkmore] {name}")

    url = "https://ipv6.lurkmo.re/"
    # r = requests.get(url + "index.php",
    #                  params={"search": name})

    # https://lurkmo.re/api.php?action=query&format=json&list=search&srsearch=%D0%B1%D0%B0%D1%82%D1%8C%D0%BA%D0%B0&srprop=size

    timedata = "speedlurk\n"
    time = datetime.now()

    r = requests.get(f"{url}api.php",
                     params={
                        "action": "query",
                        "format": "json",
                        "list": "search",
                        "srsearch": name,
                        "srlimit": 1,
                        "sprop": "size"
                     })

    if logs:
        timedata += "├─find:\n"
        loadtime = str(datetime.now() - time).split(".")
        main = loadtime[0].split(":")
        second = loadtime[1]

        timedata += f"│⠀├─seconds: {main[2]}\n"
        timedata += f"│⠀└─ms: {second}\n"

    data = json.loads(r.text)

    if len(data["query"]["search"]) == 0:
        bot.reply_to(message, "Не удалось ничего найти. Попробуйте написать ваш запрос по-другому")
        return

    name = data["query"]["search"][0]["title"]

    time = datetime.now()

    r = requests.get(url + "api.php",
                     params={
                        "action": "parse",
                        "format": "json",
                        "page": name,
                        "prop": "text|images"
                     })

    if logs:

        timedata += "├─text:\n"
        loadtime = str(datetime.now() - time).split(".")
        main = loadtime[0].split(":")
        second = loadtime[1]

        timedata += f"│⠀├─seconds: {main[2]}\n"
        timedata += f"│⠀└─ms: {second}\n"

    parse = json.loads(r.text)["parse"]
    soup = BeautifulSoup(parse["text"]["*"], 'lxml')

    div = soup

    if len(div.findAll("p")) == 0:
        redirect = soup.ol.li.a["title"]

        time = datetime.now()

        r = requests.get(url + "api.php",
                         params={
                             "action": "parse",
                             "format": "json",
                             "page": redirect,
                             "prop": "text|images"
                         })

        if logs:
            timedata += "└─image:\n"
            loadtime = str(datetime.now() - time).split(".")
            main = loadtime[0].split(":")
            second = loadtime[1]

            timedata += f" ⠀├─seconds: {main[2]}\n"
            timedata += f"⠀ └─ms: {second}\n"

        soup = BeautifulSoup(json.loads(r.text)["parse"]["text"]["*"], 'lxml')
        div = soup

    for t in div.findAll("table", {"class": "lm-plashka"}):
        t.replace_with("")

    for t in div.findAll("table", {"class": "lm-plashka-tiny"}):
        t.replace_with("")

    for t in div.findAll("table", {"class": "tpl-quote-tiny"}):
        t.replace_with("")

    for t in div.findAll("div", {"class": "gallerytext"}):
        t.replace_with("")

    bold_text = []

    for tag in div.findAll("b"):
        bold_text.append(tag.text)

    url_list = []

    for img in div.find_all("img"):
        if img["src"].find("/skins/") != -1:
            pass
        elif img["src"] == "//lurkmore.so/images/6/6b/Magnify-clip.png":
            pass
        else:
            url_list.append("https:" + img["src"])

    if logs:
        if timedata.find("image") == -1:

            timedata += "└─image:\n"
            timedata += " ⠀├─seconds: None\n"
            timedata += "⠀ └─ms: None\n"

        bot.reply_to(message, f"`{timedata}`", parse_mode="Markdown")
        return

    try:
        page_text = first if (first := div.find("p").text.strip()) \
                          else div.findAll("p", recursive=False)[1] \
                                  .text \
                                  .strip()

        page_text = page_text.replace("<", "&lt;") \
                             .replace(">", "&gt;") \
                             .replace(" )", ")") \
                             .replace("  ", " ")

        for bold in bold_text:
            page_text = re.sub(bold, f"<b>{bold}</b>", page_text, 1)

    except Exception as e:
        bot.reply_to(message, f"`{str(traceback.format_exc())}`", parse_mode="Markdown")
        bot.reply_to(message, "Не удалось найти статью")
        return

    try:
        try:
            path = f'https:{div.find(id="fullResImage")["src"]}'

            bot.send_chat_action(message.chat.id, "upload_photo")
        except:
            path = url_list[0]

            try:
                img = div.find_all("img")[0]
                filename = img["src"].split("/")[-1].replace(f'{img["width"]}px-', "")
                path = getImageInfo(url, filename)

                bot.send_chat_action(message.chat.id, "upload_photo")

            except:
                filename = parse["images"][0]
                path = getImageInfo(url, filename)

                bot.send_chat_action(message.chat.id, "upload_photo")

    except Exception as e:
        print(e)
        path = ""

    try:
        try:
            bot.send_photo(message.chat.id,
                           path,
                           caption=page_text,
                           parse_mode="HTML",
                           reply_to_message_id=message.message_id)

        except:
            try:
                bot.send_photo(message.chat.id,
                               "https:" + div.find("img", class_="thumbborder")["src"],
                               caption=page_text,
                               parse_mode="HTML",
                               reply_to_message_id=message.message_id)

            except:
                bot.send_chat_action(message.chat.id, "typing")
                bot.send_message(message.chat.id,
                                 page_text,
                                 parse_mode="HTML",
                                 reply_to_message_id=message.message_id)
    except Exception as e:
        bot.reply_to(message,
                     f"Статья недоступна\n<code>{e}</code>",
                     parse_mode="HTML")


@bot.message_handler(commands=["list"])
def commandslist(message):
    bot.reply_to(message, "/w, /van, /potatowiki, /speedlurk, /speedwiki, /speedtest, /wget")


@bot.message_handler(commands=["speedlurk"])
def speedlurk(message):
    lurk(message, True)


@bot.message_handler(commands=["speedwiki"])
def speedwiki(message):
    getWiki(message, "ru", True)


@bot.message_handler(commands=["speedtest"])
def speedtest(message):
    getWiki(message, "ru", True)
    lurk(message, True)


@bot.message_handler(commands=["test"])
def test(message):
    message_id = bot.reply_to(message, "test").message_id
    time.sleep(1)
    bot.delete_message(message.chat.id, message_id)


"""
@bot.message_handler(commands=["bashorg"])
def bashorg(message):
    num = int(message.text.replace("/bashorg@jDan734_bot ", "").replace("/bashorg ", ""))
    r = requests.get(f"https://bash.im/quote/{num}")
    soup = BeautifulSoup(r.text.replace("<br>", "БАН").replace("<br\\>", "БАН"), 'html.parser')

    print(soup.find("div", class_="quote__body").text.replace('<div class="quote__body">', "").replace("</div>", "").replace("<br\\>", "\n"))

    soup2 = BeautifulSoup(soup.find("div", class_="quote__body"), "lxml")
    bot.reply_to(message, soup2)
"""


@bot.message_handler(commands=["mrakopedia"])
def pizdec(message):
    try:
        name = message.text.split(maxsplit=1)[1]
    except:
        bot.reply_to(message, "Введите название статьи")
        return

    print(f"[Mrakopedia] {name}")

    url = "https://mrakopedia.net"
    r = requests.get(url + "/w/index.php",
                     params={"search": name})

    soup = BeautifulSoup(r.text, 'lxml')

    if soup.find("div", class_="searchresults") is None:
        pass
    else:
        div = soup.find("div", class_="searchresults")
        try:
            div.find("p", class_="mw-search-createlink").replace_with("")
            r = requests.get(url + div.find("a")["href"])
            soup = BeautifulSoup(r.text, 'lxml')
        except:
            if div.find("p", class_="mw-search-nonefound").text == "Соответствий запросу не найдено.":
                bot.reply_to(message, "Не получилось найти статью")
                return

    div = soup.find(id="mw-content-text")

    for t in div.findAll("table", {"class": "lm-plashka"}):
        t.replace_with("")

    for t in div.findAll("table", {"class": "tpl-quote-tiny"}):
        t.replace_with("")

    try:
        page_text = first if (first := div.find("p").text.strip()) else div.findAll("p", recursive=False)[1].text.strip()
    except Exception as e:
        bot.reply_to(message, "Не удалось найти статью")
        return

    try:
        try:
            path = f'{url}{div.find(id="fullResImage")["src"]}'

        except:
            path = f'{url}{div.find("a", class_="image").find("img")["src"]}'
    except:
        pass

    try:
        try:
            bot.send_photo(message.chat.id,
                           path,
                           caption=page_text,
                           parse_mode="HTML",
                           reply_to_message_id=message.message_id)
        except:
            try:
                bot.send_photo(message.chat.id,
                               "https:" + div.find("img", class_="thumbborder")["src"],
                               caption=page_text,
                               parse_mode="HTML",
                               reply_to_message_id=message.message_id)
            except:
                bot.send_message(message.chat.id, page_text, parse_mode="HTML", reply_to_message_id=message.message_id)
    except Exception as e:
        bot.reply_to(message, f"Статья недоступна\n<code>{e}</code>", parse_mode="HTML")


@bot.message_handler(commands=["to_json"])
def to_json(message):
    try:
        bot.send_message(message.chat.id,
                         message.reply_to_message.text.replace("'", "\"")
                                                      .replace("False", "false")
                                                      .replace("True", "true")
                                                      .replace("None", '"none"')
                                                      .replace("<", '"<')
                                                      .replace(">", '>"'))
    except:
        bot.reply_to(message, "Ответь на сообщение с python-кодом, который надо превравить в json")


@bot.message_handler(commands=["sha256"])
def sha256(message):
    try:
        if message.reply_to_message.text:
            bot.reply_to(message, hashlib.sha256(bytearray(message.reply_to_message.text.encode("utf-8"))).hexdigest())
        elif message.reply_to_message.document:
            file_id = message.reply_to_message.document.file_id

            document = bot.get_file(file_id)
            bot.reply_to(message, hashlib.sha256(bytearray(bot.download_file(document.file_path))).hexdigest())
        else:
            bot.reply_to(message, hashlib.sha256(bytearray(message.reply_to_message.text.encode("utf-8"))).hexdigest())
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(commands=["sticker_id"])
def get_sticker_id(message):
    try:
        bot.reply_to(message, message.reply_to_message.sticker.file_id)

    except:
        bot.reply_to(message, "Ответь на сообщение со стикером")


@bot.message_handler(commands=["delete"])
def delete(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    try:
        if message.reply_to_message.from_user.id == "1121412322":
            bot.delete_message(message.chat.id, message.reply_to_message.message_id)
    except:
        pass


"""
@bot.message_handler(commands=["delete_message"])
def delete(message):
    try:
        msgid = int(message.text.split(maxsplit=1)[1])
        bot.delete_message(message.chat.id, msgid)
        bot.reply_to(message, "Удалил")
    except:
        bot.reply_to(message, "Бан))")
"""


@bot.message_handler(commands=["generate_password"])
def password(message):
    if len(message.text.split(maxsplit=1)) == 1:
        bot.reply_to(message, "Укажите количество символов в пароле")
        return

    try:
        crypto_type = int(message.text.split(maxsplit=1)[1])
    except:
        bot.reply_to(message, "Введите число")
        return

    if crypto_type > 4096:
        bot.reply_to(message,
                     "Телеграм поддерживает сообщения длиной не больше `4096` символов",
                     parse_mode="Markdown")
        return

    elif crypto_type < 6:
        bot.reply_to(message,
                     "Пароли меньше `6` символов запрещены",
                     parse_mode="Markdown")
        return

    data = []
    password = ""
    # data.extend(list("абвгдеёжзийклмнопрстуфхцчшщъыьэюя"))
    # data.extend(list("абвгдеёжзийклмнопрстуфхцчшщъыьэюя".upper()))
    data.extend(list("abcdefghijklmnopqrstuvwxyz"))
    data.extend(list("abcdefghijklmnopqrstuvwxyz".upper()))
    data.extend(list('~!@#$%^&*()_+-=`[]\\{}|;\':"<>,./?'))
    data.extend(list("0123456789"))

    for num in range(0, crypto_type):
        password += choice(data)

    bot.reply_to(message, password)


@bot.message_handler(commands=["hided_menu"])
def start(message):
    try:
        bot.send_message(message.chat.id, texts.rules, reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_message(message.chat.id, texts.rules)


@bot.message_handler(commands=["ban"])
def ban(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    msg = message.text.replace("/ban@jDan734_bot", "").replace("/ban", "")
    try:
        bot.send_message(message.chat.id, "Бан" + msg, reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_message(message.chat.id, "Бан" + msg)


@bot.message_handler(commands=["bylo"])
def bylo(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    try:
        bot.send_message(message.chat.id, "Было", reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_message(message.chat.id, "Было")


@bot.message_handler(commands=["ne_bylo"])
def ne_bylo(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    try:
        bot.send_message(message.chat.id, "Не было", reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_message(message.chat.id, "Не было")


@bot.message_handler(commands=["pizda"])
def pizda(message):
    sendSticker(message,
                "CAACAgIAAx0CUDyGjwACAQxfCFkaHE52VvWZzaEDQwUC8FYa-wAC3wADlJlpL5sCLYkiJrDFGgQ")


@bot.message_handler(commands=["tebe_pizda"])
def tebe_pizda(message):
    sendSticker(message,
                "CAACAgIAAxkBAAILHV9qcv047Lzwp_B64lDlhtOD-2RGAAIgAgAClJlpL5VCBwPTI85YGwQ")


@bot.message_handler(commands=["net_pizdy"])
def net_pizdy(message):
    sendSticker(message,
                "CAACAgIAAx0CUDyGjwACAQ1fCFkcDHIDN_h0qHDu7LgvS8SBIgAC4AADlJlpL8ZF00AlPORXGgQ")


@bot.message_handler(commands=["xui"])
def xui(message):
    sendSticker(message,
                "CAACAgIAAx0CUDyGjwACAQ5fCFkeR-pVhI_PUTcTbDGUOgzwfAAC4QADlJlpL9ZRhbtO0tQzGgQ")


@bot.message_handler(commands=["net_xua"])
def net_xua(message):
    sendSticker(message,
                "CAACAgIAAx0CUDyGjwACAQ9fCFkfgfI9pH9Hr96q7dH0biVjEwAC4gADlJlpL_foG56vPzRPGgQ")


@bot.message_handler(commands=["xui_pizda"])
def xui_pizda(message):
    sendSticker(message,
                choice(["CAACAgIAAx0CUDyGjwACAQ5fCFkeR-pVhI_PUTcTbDGUOgzwfAAC4QADlJlpL9ZRhbtO0tQzGgQ", "CAACAgIAAx0CUDyGjwACAQxfCFkaHE52VvWZzaEDQwUC8FYa-wAC3wADlJlpL5sCLYkiJrDFGgQ"]))


def sendSticker(message, sticker_id):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    try:
        bot.send_sticker(message.chat.id,
                         sticker_id,
                         reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_sticker(message.chat.id, sticker_id)


@bot.message_handler(commands=["fake"])
def polak(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    path = "bot/images/polak.jpg" if heroku else "images/polak.jpg"

    try:
        bot.send_photo(message.chat.id, open(path, "rb"),
                       reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_photo(message.chat.id, open(path, "rb").read())


@bot.message_handler(commands=["rzaka"])
def rzaka(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    try:
        bot.send_message(message.chat.id,
                         texts.rzaka,
                         reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_message(message.chat.id, texts.rzaka)


@bot.message_handler(commands=["rzaka_time"])
def rzaka(message):
    bot.reply_to(message, str(texts.rzaka_time) + " часа")


@bot.message_handler(commands=["rzaka_full"])
def rzaka_full(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    try:
        bot.send_message(message.chat.id,
                         texts.rzaka_full,
                         reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_message(message.chat.id, texts.rzaka_full)


@bot.message_handler(commands=["detect"])
def detect_boicot(message):
    if message.text.find("бойкот") != -1:
        bot.reply_to(message, "Вы запостили информацию о бойкоте, если вы бойкотировали, то к вам приедут с паяльником")
    else:
        bot.reply_to(message, "Бойкот не обнаружен")


@bot.message_handler(commands=["random_ban", "random"])
def random(message):
    bot.reply_to(message, f"Лови бан на {randint(1, 100)} минут")


@bot.message_handler(commands=["random_color", "color"])
def random_color(message):
    options = message.text.split(" ", maxsplit=1)
    if len(options) == 1:
        randlist = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "A", "B", "C", "D", "E", "F"]

        color = ""
        for i in range(0, 6):
            color += str(choice(randlist))

        color = "#" + color

    else:
        if options[1].startswith("#"):
            color = options[1]
        else:
            bot.reply_to(message, "Вводи цвет в формате hex")
            return

    img = Photo()

    try:
        img.rectangle((0, 0), (220, 220), color)
        img.rectangle((0, 159), (220, 220), "#282C34")
        img.font(("" if heroku else "../") + "JetBrainsMono-Bold", 47)
        img.text("#DB9D63", (13, 160), color, outline=False)
        img.text("#FFF", (13, 160), "#", outline=False)
    except Exception as e:
        bot.reply_to(message,
                     f"Во время создания фото произошла ошибка\n<code>{e}</code>",
                     parse_mode="HTML")
        return

    bot.send_photo(message.chat.id,
                   img.save(),
                   caption=f"`{color}`",
                   parse_mode="Markdown")
    img.clean()


@bot.message_handler(commands=["random_putin"])
def random_putin(message):
    random_person(message, choice(["Обнуленец", "Путин", "Путен"]))


@bot.message_handler(commands=["random_lukash", "luk", "lukash"])
def random_lukash(message):
    random_person(message, choice(["Лукашенко", "Лукашеску", "3%", "Саша", "Саня"]))


def random_person(message, name):
    number = randint(0, 200)

    if number == 0:
        bot.reply_to(message, "Иди нахуй))")

    else:
        nedeli = number / 7
        date = choice(["дней", "месяцев"])

        if date == "дней":
            true_date = prettyword(number, ["день", "дня", "дней"])

        elif date == "месяцев":
            true_date = prettyword(number, ["месяц", "месяца", "месяцев"])

        if number % 7 == 0:
            bot.reply_to(message, f'{name} уйдет через {int(nedeli)} {prettyword(int(nedeli), ["неделя", "недели", "недель"])}')
        else:
            print(number % 7)
            bot.reply_to(message, f'{name} уйдет через {int(nedeli)} {prettyword(int(nedeli), ["неделя", "недели", "недель"])} и {int(number % 7)} {prettyword(int(number % 7), ["день", "дня", "дней"])}')


@bot.message_handler(commands=["da_net", "r"])
def da_net(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    try:
        bot.send_message(message.chat.id, choice(["Да", "Нет"]), reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_message(message.chat.id, choice(["Да", "Нет"]))


@bot.message_handler(commands=["message"])
def msg(message):
    if message.chat.id == 795449748:
        try:
            params = message.text.split(maxsplit=2)
            bot.send_message(params[1], params[2])
        except Exception as e:
            bot.reply_to(message, f"`{e}`", parse_mode="Markdown")


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


digits_pattern = re.compile(r'.{,}', re.MULTILINE)
@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_text(query):
    try:
       matches = re.match(digits_pattern, query.query)

    except AttributeError as ex:
        return

    try:
        wiki = Wikipedia("ru")
        q = matches.group()
        r = wiki.search(q, 5)
        print(q)
        btns = []
        for page in r:
            p = wiki.getPage(page[0])
            img = wiki.getImageByPageName(page[0], 75)
            full_img = wiki.getImageByPageName(page[0])
            print(page[0])
            print(img)
            t1 = re.sub("<b>", f'<a href="{full_img}">', wiki.parsePage(p), 1)

            t2 = re.sub("</b>", "</a>", t1, 1)
            print(t2)
            if img != -1 and full_img != -1:
                btns.append(telebot.types.InlineQueryResultArticle(
                        id=page[1], title=page[0],
                        # Описание отображается в подсказке,
                        # message_text - то, что будет отправлено в виде сообщения
                        description=p.text[:100],
                        input_message_content=telebot.types.InputTextMessageContent(
                        message_text=t2,
                        parse_mode="HTML"),
                        thumb_url=img, thumb_width=48, thumb_height=48
                ))
            else:
                btns.append(telebot.types.InlineQueryResultArticle(
                        id=page[1], title=page[0],
                        # Описание отображается в подсказке,
                        # message_text - то, что будет отправлено в виде сообщения
                        description=p.text[:100],
                        input_message_content=telebot.types.InputTextMessageContent(
                        message_text=wiki.parsePage(p),
                        parse_mode="HTML"),
                        thumb_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/75px-Wikipedia-logo-v2.svg.png", thumb_width=48, thumb_height=48
                ))

        bot.answer_inline_query(query.id, btns)
    except Exception as e:
        print("{!s}\n{!s}".format(type(e), str(e)))


@bot.message_handler(content_types=['document', 'video'],
                     func=lambda message: message.chat.id == -1001189395000)
def delete_w10(message):
    try:
        if message.video.file_size == 842295 or \
           message.video.file_size == 912607:
            bot.delete_message(message.chat.id, message.message_id)
    except:
        pass


try:
    bot.polling()

except:
    bot.send_message("795449748",
                     f"`{str(traceback.format_exc())}`",
                     parse_mode="Markdown")
