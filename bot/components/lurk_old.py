from .token import bot
from .lib.lurkmore import Lurkmore
from bs4 import BeautifulSoup

import requests

L = Lurkmore()


def getImageInfo(url, filename):
    r = requests.get(url + "index.php",
                     params={
                         "search": f"Файл:{filename}"
                     })

    soup = BeautifulSoup(r.text, 'lxml')

    return "https:" + soup.find("div", id="file").a.img["src"]


@bot.message_handler(commands=["lurk_old"])
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
    p = L.getPage(name)

    # r = requests.get(url + "api.php",
    #                  params={
    #                     "action": "parse",
    #                     "format": "json",
    #                     "page": name,
    #                     "prop": "images",
    #                     "section": 0,
    #                     "redirects": True
    #                  })

    div = BeautifulSoup(p, 'lxml')

    url_list = []

    for img in div.find_all("img"):
        if img["src"].find("/skins/") != -1:
            pass
        elif img["src"] == "//lurkmore.so/images/6/6b/Magnify-clip.png":
            pass
        else:
            url_list.append("https:" + img["src"])

    print(url_list)
    for url in url_list:
        bot.send_photo(message.chat.id, url)

    page_text = L.parse(p)

    try:
        try:
            path = f'https:{div.find(id="fullResImage")["src"]}'
            print(path)

            bot.send_chat_action(message.chat.id, "upload_photo")
        except:
            path = url_list[0]

            try:
                img = div.find_all("img")[0]
                filename = img["src"].split("/")[-1].replace(f'{img["width"]}px-', "")
                print(img)
                path = getImageInfo(url, filename)

                bot.send_chat_action(message.chat.id, "upload_photo")

            except:
                filename = L.getImagesList("Путин")[0]
                print(filename)
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
