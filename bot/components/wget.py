from .token import bot
from .lib.fixHTML import fixHTML
from datetime import datetime
import sys
import requests


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

    except:
        bot.reply_to(message,
                     '<code>Ошибка, тебе бан))))</code>',
                     parse_mode="HTML")


@bot.message_handler(["wget", "r", "request"])
def wget(message):
    if len(message.text.split(maxsplit=1)) == 1:
        bot.reply_to(message, "Напиши ссылку")
        return

    time = datetime.now()
    url = message.text.split(maxsplit=1)[1]

    blacklist = [
        "mb",
        ".zip",
        ".7",
        ".dev",
        ".gz",
        "98.145.185.175",
        ".avi",
        "movie",
        "release",
        ".dll",
        "localhost",
        ".bin",
        "0.0.0.1",
        "repack",
        "download"
    ]

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
