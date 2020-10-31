from .token import bot
from .lib.lurkmore import Lurkmore
from bs4 import BeautifulSoup

import requests
import traceback
import json
import re

L = Lurkmore()


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

    data = L.opensearch(name)

    if len(data) == 0:
        bot.reply_to(message, "Не удалось ничего найти. Попробуйте написать ваш запрос по-другому")
        return

    name = data[0]

    r = requests.get(url + "api.php",
                     params={
                        "action": "parse",
                        "format": "json",
                        "page": name,
                        "prop": "text|images",
                        "section": 0,
                        "redirects": True
                     })

    parse = json.loads(r.text)["parse"]
    soup = BeautifulSoup(parse["text"]["*"], 'lxml')

    div = soup

    # if len(div.findAll("p")) == 0:
    #     redirect = soup.ol.li.a["title"]

    #     r = requests.get(url + "api.php",
    #                      params={
    #                          "action": "parse",
    #                          "format": "json",
    #                          "page": redirect,
    #                          "prop": "text|images"
    #                      })

    #     soup = BeautifulSoup(json.loads(r.text)["parse"]["text"]["*"], 'lxml')
    #     div = soup

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

    try:
        try:
            page_text = first if (first := div.find("p").text.strip()) \
                              else div.findAll("p")[1] \
                                      .text \
                                      .strip()

        except:
            page_text = first if (first := div.find("p").text.strip()) \
                              else div.findAll("p")[0] \
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
