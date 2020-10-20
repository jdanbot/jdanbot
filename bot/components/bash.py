from .token import bot
from bs4 import BeautifulSoup

import requests


@bot.message_handler(commands=["bashorg", "bash", "b"])
def bashorg(message):
    params = message.text.split(maxsplit=2)
    if len(params) == 1:
        r = requests.get("https://bash.im/random")
    else:
        try:
            num = int(params[1])
        except ValueError:
            bot.reply_to(message, "Введи число")
            return

        r = requests.get(f"https://bash.im/quote/{num}")

    soup = BeautifulSoup(r.text.replace("<br>", "\n"), 'lxml')
    soup2 = soup.find("div", class_="quote__body")

    for tag in soup2.find_all("div", {"class": "quote__strips"}):
        tag.replace_with("")

    soup2 = soup2 .text \
                  .replace('<div class="quote__body">', "") \
                  .replace("</div>", "") \
                  .replace("<br\\>", "\n")
    bot.reply_to(message, soup2)
