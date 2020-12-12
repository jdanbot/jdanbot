from .token import bot
from bs4 import BeautifulSoup
import requests


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
