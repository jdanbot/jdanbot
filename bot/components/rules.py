from .token import bot
import json
import requests


def getRules(page):
    r = requests.get(f"https://api.telegra.ph/getPage/{page}")
    rules = json.loads(r.text)["result"]
    return rules


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
