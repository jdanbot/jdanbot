from .token import bot
import traceback
import re
import requests
import telebot
import time
import json


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
