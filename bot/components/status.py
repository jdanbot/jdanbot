from .token import bot, heroku
from datetime import datetime
import platform


start_time = datetime.now()


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

    h = main[0]
    h = "0" + h if len(h) == 1 else h

    text =  f"status:\n"
    text += f"├─status: 👍\n"
    text += f"├─heroku: {heroku}\n"
    text += f"├─uptime: {h}:{main[1]}:{main[2]}\n"
    text += f"├─machine: {platform.machine()}\n"
    text += f"└─os: {platform.system()}\n"

    text = text.replace("False", "❌") \
               .replace("True", "✅")

    bot.reply_to(message,
                 f"`{text}`",
                 parse_mode="Markdown")
