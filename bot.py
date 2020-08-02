import telebot
import re
from random import randint, choice
from nword import *
import os
import json
import traceback
import hashlib
#from tree_lib import *
import wikipediaapi as wikipedia
from bs4 import BeautifulSoup
import requests

rules = """
/ban - отправляет "Бан"
/bylo - отправляет "Было"
/ne_bylo - отправляет "Не было"
/fake - отправляет фото с джонами/поляками
/pizda - отправляет мем "пизда"
/net_pizdy - отправляет мем "нет пизда"
/xui - отправляет мем "хуй" 
"""

if "TOKEN_HEROKU" in os.environ:
    bot = telebot.TeleBot(os.environ["TOKEN_HEROKU"])

elif "TOKEN" in os.environ:
    bot = telebot.TeleBot(os.environ["TOKEN"])

else:
    with open("./token.txt") as token:
        bot = telebot.TeleBot(token.read())

# @bot.message_handler(commands=["wikiru"])
# def wikiru(message):
#     print(message.text.replace("/wikiru@jDan734_bot ", "").replace("/wikiru ", ""))
#     name = message.text.replace("/wikiru@jDan734_bot ", "").replace("/wikiru ", "")
#     wiki = wikipedia.Wikipedia("ru")
#     bot.send_message(message.chat.id, re.split("\\n", wiki.page(name).text)[0])
#     #except:
#     #    bot.send_message(message.chat.id, "Отправьте название статьи")

@bot.message_handler(commands=["wikiru", "wikiru2"])
def wikiru(message):
    getWiki(message, "ru")

@bot.message_handler(commands=["wikien"])
def wikien(message):
    getWiki(message, "en")

@bot.message_handler(commands=["wikide"])
def wikide(message):
    getWiki(message, "de")

@bot.message_handler(commands=["wikipl"])
def wikipl(message):
    getWiki(message, "pl")

@bot.message_handler(commands=["wikiua", "wikiuk"])
def wikiua(message):
    getWiki(message, "uk")

@bot.message_handler(commands=["wikibe"])
def wikibe(message):
    getWiki(message, "be")

@bot.message_handler(commands=["wikies"])
def wikies(message):
    getWiki(message, "es")

def getWiki(message, lang="ru"):
    name = message.text.replace("/wikiru2@jDan734_bot ", "").replace("/wikiru2 ", "").replace("/wikiru@jDan734_bot ", "").replace("/wikiru ", "").replace("/wikide@jDan734_bot ", "").replace("/wikide ", "").replace("/wikien@jDan734_bot ", "").replace("/wikien ", "").replace("/wikipl@jDan734_bot ", "").replace("/wikipl ", "").replace("/wikiua@jDan734_bot ", "").replace("/wikiua ", "").replace("/wikipl@jDan734_bot ", "").replace("/wikipl ", "").replace("/wikiuk@jDan734_bot ", "").replace("/wikiuk ", "").replace("/wikibe@jDan734_bot ", "").replace("/wikibe ", "").replace("/wikies@jDan734_bot ", "").replace("/wikies ", "")
    print(name)

    url = "https://ru.wikipedia.org"
    r = requests.get(url + "/wiki/" + name.replace(" ", "_"))

    page = {}
    wiki = wikipedia.Wikipedia(lang)


    page["page"] = wiki.page(name).text
    page["page"] = re.split("\\n", page["page"])[0]

    page["page"] = f'<b>{page["page"].replace("(", "</b>(", 1)}'
    if page["page"].find("</b>") == -1:
        page["page"] = f'{page["page"].replace("—", "</b>—", 1)}'

    soup = BeautifulSoup(r.text, 'lxml')
    #bot.send_photo(message, "https:" + page["image_url"], caption=page["page"], parse_mode="HTML")
    try:
        try:
            page["image_url"] = soup.find("td", class_="infobox-image").span.a.img.get("src")
            print("https:" + page["image_url"])
            #page["page"] = soup.find("div", id="mw-content-text").find("div", class_="mw-parser-output").find_all("p")[0].text

            bot.send_photo(message.chat.id, "https:" + page["image_url"], caption=page["page"], parse_mode="HTML", reply_to_message_id=message.message_id)
            #bot.reply_to(message, "https:" + page["image_url"], caption=page["page"], parse_mode="HTML")
        except:
            try:
                page["image_url"] = soup.find("td", class_="infobox-image").span.span.a.img.get("src")
                print("https:" + page["image_url"])
                #page["page"] = soup.find("div", id="mw-content-text").find("div", class_="mw-parser-output").find_all("p")[0].text

                bot.send_photo(message.chat.id, "https:" + page["image_url"], caption=page["page"], parse_mode="HTML", reply_to_message_id=message.message_id)
            except:
                #bot.send_message(message.chat.id, page["page"])
                bot.reply_to(message, page["page"], parse_mode="HTML")
    except:
        bot.reply_to(message, "Такой статьи нет")

# @bot.message_handler(commands=["to_tree_my"])
# def to_tree(message):
#     bot.send_message(message.chat.id, "json\n" + dict_to_tree(json.loads(message.reply_to_message.text)), parse_mode="HTML")

# @bot.message_handler(commands=["to_tree_my_info"])
# def to_tree(message):
#     bot.send_message(message.chat.id, message.reply_to_message)

@bot.message_handler(commands=["lurk"])
def lurk(message):
    name = message.text.replace("/lurk@jDan734_bot ", "").replace("/lurk ", "")
    url = "https://lurkmore.to/"
    r = requests.get(url + "index.php",
                     params={"search": name})

    soup = BeautifulSoup(r.text, 'lxml')

    #print(dir(soup.find("div", id="mw-content-text").find("table")))
    #soup.find("div", id="mw-content-text").find("table").remove()
    page = soup.find(id="mw-content-text").find("p")
    for tag in soup.find(id="mw-content-text").find_all("p"):
        if tag.get("class"):
            pass
        elif tag.parent.get("class") == ["gallerytext"]:
            pass
        else:
            page = tag
            break

    page_text = f'<b>{page.text.replace("(", "</b>(", 1)}'
    if page.find("</b>") == -1:
        page = f'{page.text.replace("—", "</b>—", 1)}'
    try:
        try:
            image_url = soup.find(class_=["thumb", "tright"]).find("img").get("src")
            bot.send_photo(message.chat.id, "https:" + image_url, caption=page_text, parse_mode="HTML", reply_to_message_id=message.message_id)
        except:
            bot.send_message(message.chat.id, page_text, parse_mode="HTML", reply_to_message_id=message.message_id)
    except:
        bot.send_message(message.chat.id, "Статья недоступна")

# @bot.message_handler(commands=["bashorg"])
# def bashorg(message):
#     num = int(message.text.replace("/bashorg@jDan734_bot ", "").replace("/bashorg ", ""))
#     r = requests.get(f"https://bash.im/quote/{num}")
#     soup = BeautifulSoup(r.text.replace("<br>", "БАН").replace("<br\\>", "БАН"), 'html.parser')

#     print(soup.find("div", class_="quote__body").text.replace('<div class="quote__body">', "").replace("</div>", "").replace("<br\\>", "\n"))

#     soup2 = BeautifulSoup(soup.find("div", class_="quote__body"), "lxml")
#     bot.reply_to(message, soup2)

@bot.message_handler(commands=["to_json"])
def to_json(message):
    bot.send_message(message.chat.id, message.reply_to_message.text.replace("'", "\"").replace("False", "false").replace("True", "true").replace("None", '"none"').replace("<", '"<').replace(">", '>"'))

@bot.message_handler(commands=["sha256"])
def sha(message):
    if message.reply_to_message.text is None:
        bot.reply_to(message, "Это текст? Ответьте на сообщение с текстом")
    else:
        bot.reply_to(message, hashlib.sha256(bytearray(message.reply_to_message.text.encode("utf-8"))).hexdigest())

@bot.message_handler(commands=["delete"])
def delete(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    try:
        #bot.send_message(message.chat.id, message.reply_to_message)
        bot.delete_message(message.chat.id, message.reply_to_message.message_id)
    except:
        pass

@bot.message_handler(commands=["delete_message"])
def delete(message):
    try:
        msgid = int(message.text.split(maxsplit=1)[1])
        bot.delete_message(message.chat.id, msgid)
        bot.reply_to(message, "Удалил")
    except:
        bot.reply_to(message, "Бан))")


@bot.message_handler(commands=["generate_password"])
def password(message):
    try:
        crypto_type = int(message.text.split(maxsplit=1)[1])
        #print(crypto_type)
        if crypto_type > 4096:
            bot.reply_to(message, "Телеграм поддерживает сообщения длиной не больше `4096` символов", parse_mode="Markdown")
            0 / 0
    except:
        crypto_type = 256

    data = []
    password = ""
    # data.extend(list("абвгдеёжзийклмнопрстуфхцчшщъыьэюя"))
    # data.extend(list("абвгдеёжзийклмнопрстуфхцчшщъыьэюя".upper()))
    data.extend(list("abcdefghijklmnopqrstuvwxyz"))
    data.extend(list("abcdefghijklmnopqrstuvwxyz".upper()))
    data.extend(list('~!@#$%^&*()_+-=`[]\\{}|;\':"<>,./?'))
    data.extend(list("0123456789"))
    #bot.reply_to(message, f"<code>{json.dumps(data)}</code>", parse_mode="HTML")
    #bot.reply_to(message, json.dumps(data))

    for num in range(0, crypto_type):
        password += choice(data)

    bot.reply_to(message, password)
    #print(data)
	
@bot.message_handler(commands=["start", "help"])
def start(message):
    # try:
    #     bot.delete_message(message.chat.id, message.message_id)
    # except:
    #     True
    try:
        bot.send_message(message.chat.id, rules, reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_message(message.chat.id, rules)

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
    #print(message)
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        True

    try:
        bot.send_message(message.chat.id, "Было", reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_message(message.chat.id, "Было")

@bot.message_handler(commands=["ne_bylo"])
def ne_bylo(message):
    #print(message)
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
    stid = "CAACAgIAAx0CUDyGjwACAQxfCFkaHE52VvWZzaEDQwUC8FYa-wAC3wADlJlpL5sCLYkiJrDFGgQ"
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    try:
        bot.send_sticker(message.chat.id, stid, reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_sticker(message.chat.id, stid)


@bot.message_handler(commands=["net_pizdy"])
def net_pizdy(message):
    stid = "CAACAgIAAx0CUDyGjwACAQ1fCFkcDHIDN_h0qHDu7LgvS8SBIgAC4AADlJlpL8ZF00AlPORXGgQ"
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    try:
        bot.send_sticker(message.chat.id, stid, reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_sticker(message.chat.id, stid)

@bot.message_handler(commands=["xui"])
def xui(message):
    stid = "CAACAgIAAx0CUDyGjwACAQ5fCFkeR-pVhI_PUTcTbDGUOgzwfAAC4QADlJlpL9ZRhbtO0tQzGgQ"
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    try:
        bot.send_sticker(message.chat.id, stid, reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_sticker(message.chat.id, stid)

@bot.message_handler(commands=["net_xua"])
def net_xua(message):
    stid = "CAACAgIAAx0CUDyGjwACAQ9fCFkfgfI9pH9Hr96q7dH0biVjEwAC4gADlJlpL_foG56vPzRPGgQ"
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    try:
        bot.send_sticker(message.chat.id, stid, reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_sticker(message.chat.id, stid)

@bot.message_handler(commands=["fake"])
def polak(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    try:
        bot.send_photo(message.chat.id, open("images/polak.jpg", "rb"), reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_photo(message.chat.id, open("images/polak.jpg", "rb").read())

@bot.message_handler(commands=["rzaka"])
def rzaka(message):
    #print(message)
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        True

    text = r"РЖАКА-СМЕЯКА 🤣🤣🤣🤣😋😋😋😋😋😋СРАЗУ ВИДНО РУССКОГО ЧЕЛОВЕКА😃😃😃😃😃🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺👍👍👍👍ТУПЫЕ ПЕНДОСЫ В СВОЕЙ ОМЕРИКЕ ДО ТАКОГО БЫ НЕ ДОДУМАЛИСЬ😡😡😡😡😡😡👎👎👎👎👎🇺🇸🇺🇸🇺🇸🇺🇸🇺🇸🇺🇸"

    try:
        bot.send_message(message.chat.id, text, reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["rzaka_full"])
def rzaka_full(message):
    #print(message)
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        True

    text = r"РЖАКА-СМЕЯКА 🤣🤣🤣🤣😋😋😋😋😋😋СРАЗУ ВИДНО РУССКОГО ЧЕЛОВЕКА😃😃😃😃😃🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺👍👍👍👍ТУПЫЕ ПЕНДОСЫ В СВОЕЙ ОМЕРИКЕ ДО ТАКОГО БЫ НЕ ДОДУМАЛИСЬ😡😡😡😡😡😡👎👎👎👎👎🇺🇸🇺🇸🇺🇸🇺🇸🇺🇸🇺🇸РОССИЯ ВПЕРЕД😊😊😊😊😊😊😃😃😃😃😃😃😋😋😋😋🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺🇷🇺АХАХАХАХАХ😃😃😃😃😃СМЕШНО ПОШУТИЛ ЧУВАЧОК👉👋👍👍👍👍👍ТАКОЕ МОЖНО УВИДЕТЬ ТОЛЬКО В РОССИИ ✌️✌️😲😲😲 ХААХАХА ВОТ УМОРА🤣🤣🤣🤣АЖ АМЕРИКА ВЗОРВАЛАСЬ ОТ СМЕХА😜😜😜😜😜😜😜ВСЯ ЕВРОПА В ШОКЕ🤙🤙🤙🤙🤙🤙🤙АХХАХАХАХА БЛИН НЕ МОГУ ОСТАНОВИТЬСЯ СМЕЮСЬ КАТАЮСЬ ПО ПОЛУ😬😬😬😵😵😵😵😵ВОТ ЭТО ШУТКА РЖАКА СМЕЯЛИСЬ ВСЕЙ МАРШРУТКОЙ РЖАЛА 848393938347292929647492918363739304964682010 ЧАСОВ РЖОМБА ПРЯМА НЕРЕАЛЬНАЯ РЖАКА ШУТКА 😂😂😂😂😂😂😂😂🤔😂😂😹😹😹😹😹😹😹😹😹😂😂😂😂👍👍👍👍👍👍👍👍👍👍АХАХА , КАК СМЕШНО !!!!! Я НЕ МОГУ, ПОМОГИТЕ , ЗАДЫХАЮСЬ ОТ СМЕХА 😂🤣🤣😄🤣😂🤣🤣🤣 СПАСИБО , ВЫ СДЕЛАЛИ МОЙ ДЕНЬ !!! КАК ЖЕ ОРИГИНАЛЬНО !!! Я В ВОСТОРГЕ!!!!!!😀😃😀😃🤣😁🤣🤣🤣🤣🤣😀🤣😀😀🤣🤣😀🤣😀🤣😀🤣😀🤣😀🤣😀😀🤣😀🤣😁🤣😁🤣😁🤣😁😁🤣😁"

    try:
        bot.send_message(message.chat.id, text, reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["genfile"])
def genfile(message):
    pass

@bot.message_handler(commands=["detect"])
def detect(message):
    if message.text.find("бойкот") != -1:
        bot.reply_to(message, "Вы запостили информацию о бойкоте, если вы бойкотировали, то к вам приедут с паяльником")
    else:
        bot.reply_to(message, "Бойкот не обнаружен")

@bot.message_handler(commands=["random_ban", "random"])
def random(message):
    bot.reply_to(message, f"Лови бан на {randint(1, 100)} минут")

@bot.message_handler(commands=["random_putin"])
def random_putin(message):
    number = randint(1, 500)
    date = choice(["дней", "месяцев", "лет"])

    if date == "дней":
        true_date = nword(number, ["день", "дня", "дней"])
    elif date == "месяцев":
        true_date = nword(number, ["месяц", "месяца", "месяцев"])
    elif date == "лет":
        true_date = nword(number, ["год", "года", "лет"])


    bot.reply_to(message, f'Путин уйдет через {number} {true_date}')
    #bot.reply_to(message, bot.reply_to(message, f'Путин уйдет через {randint(1, 500)} {choice(["дней", "месяцев", "лет", "тысячелетий"])}').message_id)

@bot.message_handler(commands=["da_net"])
def da_net(message):
    bot.reply_to(message, choice(["Да", "Нет"]))

@bot.message_handler(content_types=['text'])
def detect(message):
    if message.text.find("бойкот") != -1:
        bot.reply_to(message, "Вы запостили информацию о бойкоте, если вы бойкотировали, то к вам приедут с паяльником")

    if message.text.find("когда уйдет путин") != -1:
        #bot.reply_to(message, f'Путин уйдет через {randint(1, 500)} {choice(["дней", "месяцев", "лет", "тысячелетий"])}')
        random_putin(message)  

@bot.message_handler(content_types=["new_chat_members"])
def john(message):
    bot.reply_to(message, f'{choice(["Поляк", "Джон", "Александр Гомель", "Иван", "УберКац", "Яблочник"])}?')

try:
    bot.polling()
except:
    #bot.send_message("-1001335444502", f"`{str(traceback.format_exc())}`", parse_mode="Markdown")
    pass