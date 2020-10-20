from .token import bot
from bs4 import BeautifulSoup

import requests


@bot.message_handler(commands=["bashorg", "bash", "b"])
def bashorg(message):
    params = message.text.split(maxsplit=2)
    if len(params) == 1:
        bot.reply_to(message, "Введи номер цитаты из башорга")

    try:
        num = int(params[1])
    except ValueError:
        bot.reply_to(message, "Введи число")
        return

    try:
        r = requests.get(f"https://bash.im/quote/{num}")
    except:
        bot.reply_to(message, "Не удалось загрузить цитату")
        return

    soup = BeautifulSoup(r.text.replace("<br>", "\n"), 'lxml')
    soup2 = soup.find("div", class_="quote__body")

    for tag in soup2.find_all("div", {"class": "quote__strips"}):
        tag.replace_with("")

    soup2 = soup2 .text \
                  .replace('<div class="quote__body">', "") \
                  .replace("</div>", "") \
                  .replace("<br\\>", "\n")
    bot.reply_to(message, soup2)
