import telebot
import re
from random import randint, choice
from prettyword import *
import os
import json
import traceback
import hashlib
#from tree_lib import *
import wikipediaapi as wikipedia
from bs4 import BeautifulSoup
import requests
import math
from PIL import Image, ImageDraw, ImageFont
from decimal import *
import urllib
#import youtube_dl

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


separator = "/" if os.name == "posix" or os.name == "macos" else "\\"

# @bot.message_handler(commands=["wikiru"])
# def wikiru(message):
#     print(message.text.replace("/wikiru@jDan734_bot ", "").replace("/wikiru ", ""))
#     name = message.text.replace("/wikiru@jDan734_bot ", "").replace("/wikiru ", "")
#     wiki = wikipedia.Wikipedia("ru")
#     bot.send_message(message.chat.id, re.split("\\n", wiki.page(name).text)[0])
#     #except:
#     #    bot.send_message(message.chat.id, "Отправьте название статьи")

#bot.leave_chat(-1001189395000)

#bot.delete_message(-1001176998310, 164427)

@bot.message_handler(["if"])
def if_(message):
    options = message.text.split()
    try:
        bot.reply_to(message, f"<code>{options[1]}</code> == <code>{options[2]}</code>: <b>{options[1] == options[2]}</b>", parse_mode="HTML")
    except:
        bot.reply_to(message, "Напиши аргументы :/")


# @bot.message_handler(["youtube"])
# def downloadYoutube(message):
#     try:
#         message.reply_to_message.text.replace(" ", "").replace(";", "")
#         print("Text")
#     except:
#         bot.reply_to(message, "Ответь на сообщение с ссылкой")
#         return

#     src = f"{os.path.dirname(os.path.abspath(__file__))}{separator}"

#     with youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s', "format": "18"}) as ydl:
#         video = ydl.download([message.reply_to_message.text])
#     print(src + "M1a2JBhacz8.mp4")
#     bot.send_video(message.chat.id, open(src + "M1a2JBhacz8.mp4" , "rb"))

@bot.message_handler(commands=["preview"])
def preview(message):
    try:
        try:
            bot.send_photo(message.chat.id, f"https://img.youtube.com/vi/{message.reply_to_message.text.replace('&feature=share', '').split('/')[-1]}/maxresdefault.jpg")
        except:
            bot.send_photo(message.chat.id, 
                           f'https://img.youtube.com/vi/{urllib.parse.parse_qs(urllib.parse.urlparse(message.reply_to_message.text).query)["v"][0]}/maxresdefault.jpg')
    except Exception as e:
        print(e)
        bot.reply_to(message, "Не получилось скачать превью")

@bot.message_handler(commands=["resize"])
def resize(message):
    try:
        try:
            options = message.text.split()
        except:
            options = []
            options[0] = message.text
        print(options)

        try:
            int(options[1])
        except:
            options.extend([100000])

        try:
            int(options[2])
        except:
            options.extend([100000])

        src = f"{os.path.dirname(os.path.abspath(__file__))}{separator}cache{separator}"

        try:
            photo = bot.get_file(message.reply_to_message.photo[-1].file_id)
            file_id = message.reply_to_message.photo[-1].file_id
        except:
            photo = bot.get_file(message.reply_to_message.document.file_id)
            file_id = message.reply_to_message.document.file_id

        file = bot.download_file(photo.file_path)

        try:
            os.remove(src + file_id)
        except:
            pass

        with open(src + file_id + ".jpg", "wb") as new_file:
            new_file.write(file)
        img = Image.open(src + file_id + ".jpg")
        img.thumbnail((int(options[1]), int(options[1])))
        img.save(src + file_id + "_saved.jpg")
        bot.send_photo(message.chat.id, open(src + file_id + "_saved.jpg", "rb"))
        os.remove(src + file_id + "_saved.jpg")
        os.remove(src + file_id + ".jpg")

    except Exception as e:
        bot.reply_to(message, f"`{e}`", parse_mode="Markdown")


@bot.message_handler(commands=["text"])
def text(message):
    #text = message.text.replace("/text@jDan734_bot ", "").replace("/text ", "")
    params = message.text.split()
    print(params)
    # if True:
    try:
        int(params[3].split("x")[0])
        params = message.text.split(maxsplit=4)
        text = params[len(params) - 1]
    except:
        params = message.text.split(maxsplit=1)
        text = params[1]
    # elif len(params) == 1:
    #     bot.reply_to(message, "Ответь на фото, на которое нужно добавить текст")
    #     return
    # else:
    #     params = message.text.split(maxsplit=1)
    #     text = params[1]

    src = f"{os.path.dirname(os.path.abspath(__file__))}{separator}cache{separator}"

    try:
        try:
            photo = bot.get_file(message.reply_to_message.photo[-1].file_id)
            file_id = message.reply_to_message.photo[-1].file_id
        except:
            photo = bot.get_file(message.reply_to_message.document.file_id)
            file_id = message.reply_to_message.document.file_id
        file = bot.download_file(photo.file_path)

        try:
            os.remove(src + file_id + ".jpg")
        except:
            pass

        with open(src + file_id + "_copy.jpg", "wb") as new_file:
            new_file.write(file)

        with open(src + file_id + ".jpg", "wb") as new_file:
            new_file.write(file)

        img = Image.open(src + file_id + ".jpg")


        idraw = ImageDraw.Draw(img)


        # font = ImageFont.truetype("JetBrainsMono.ttf", size=28)
        # idraw.text((4, 4), text, font=font)

        # font = ImageFont.truetype("JetBrainsMono.ttf", size=27)
        # idraw.text((6, 6), text, font=font)
        try:
            xy = params[3].split("x")
        except:
            xy = [100, 100]

        try:
            x = int(xy[0])
        except:
            x = 100

        try:
            y = int(xy[1])
        except:
            y = 100

        try:
            size = int(params[1])
        except:
            size = 100

        if size > 1000:
            size = 1000

        #font = ImageFont.truetype("NotoSans-Regular.ttf", size=size)
        #font = ImageFont.truetype("Apple Color Emoji.ttf", size=size)
        # idraw.text((7, 10), text, font=font, fill=(0, 0, 0, 0))


        shadowcolor = "white"

        try:
            try:
                fillcolor = params[2].split(",")
                fillcolor = fillcolor.extend(["0"])
                fillcolor = [int(num) for num in fillcolor]
                fillcolor = tuple(fillcolor)
            except:
                fillcolor = params[2]
        except:
            fillcolor = "black"

        font = ImageFont.truetype("OpenSans-Bold.ttf", size=size)

        p = 3

        idraw.text((x-p, y), text, font=font, fill=shadowcolor)
        idraw.text((x+p, y), text, font=font, fill=shadowcolor)
        idraw.text((x, y-p), text, font=font, fill=shadowcolor)
        idraw.text((x, y+p), text, font=font, fill=shadowcolor)

        # thicker border
        idraw.text((x-p, y-p), text, font=font, fill=shadowcolor)
        idraw.text((x+p, y-p), text, font=font, fill=shadowcolor)
        idraw.text((x-p, y+p), text, font=font, fill=shadowcolor)
        idraw.text((x+p, y+p), text, font=font, fill=shadowcolor)


        try:
            idraw.text((x, y), text, font=font, fill=fillcolor)
        except:
            idraw.text((x, y), text, font=font, fill="black")

        img.save(src + file_id + "_text.png", "PNG", dpi=[300,300], quality=100)
        bot.send_photo(message.chat.id, open(src + file_id + "_text.png", "rb"))

        os.remove(src + file_id + "_text.png")
        os.remove(src + file_id + ".jpg")

            #os.remove(src + message.reply_to_message.photo[0].file_id)
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(commands=["rectangle"])
def rectangle(message):
    #text = message.text.replace("/text@jDan734_bot ", "").replace("/text ", "")
    params = message.text.split(maxsplit=4)
    print(params)
    try:
        params[2]

        src = f"{os.path.dirname(os.path.abspath(__file__))}{separator}cache{separator}"

        try:
            photo = bot.get_file(message.reply_to_message.photo[-1].file_id)
        except:
            photo = bot.get_file(message.reply_to_message.document.thumb.file_id)
        file = bot.download_file(photo.file_path)

        try:
            os.remove(src + message.reply_to_message.photo[-1].file_id + ".jpg")
        except:
            pass

        with open(src + message.reply_to_message.photo[-1].file_id + "_copy.jpg", "wb") as new_file:
            new_file.write(file)

        with open(src + message.reply_to_message.photo[-1].file_id + ".jpg", "wb") as new_file:
            new_file.write(file)

        img = Image.open(src + message.reply_to_message.photo[-1].file_id + ".jpg")


        idraw = ImageDraw.Draw(img)


        try:
            optsize = params[2].split("x")
            optsize1 = params[3].split("x")

            size = (int(optsize[0]), int(optsize[1]))
            size1 = (int(optsize1[0]), int(optsize1[0]))
        except:
            optsize = params[2].split(".")
            optsize1 = params[3].split(".")

            size = (int(optsize[0]), int(optsize[1]))
            size1 = (int(optsize1[0]), int(optsize1[0]))

        idraw.rectangle((size, size1), fill=params[1])
        #except:
        #    idraw.text((x, y), text, font=font, fill="black")

        img.save(src + message.reply_to_message.photo[-1].file_id + "_text.png", "PNG", dpi=[300,300], quality=100)
        bot.send_photo(message.chat.id, open(src + message.reply_to_message.photo[-1].file_id + "_text.png", "rb"))

        os.remove(src + message.reply_to_message.photo[-1].file_id + "_text.png")
        os.remove(src + message.reply_to_message.photo[-1].file_id + ".jpg")

                #os.remove(src + message.reply_to_message.photo[0].file_id)
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(commands=["sqrt"])
def sqrt(message):
    try:
        num = float(message.text.split()[1])
        res = math.sqrt(num)

        try:
            res = float(res)
        except:
            res = int(res)


        bot.reply_to(message, f"`{res}`", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"`{e}`", parse_mode="Markdown")

@bot.message_handler(commands=["calc"])
def calc(message):
    options = message.text.split(maxsplit=1)[1].replace(" ", "").replace(",", ".").replace("pi", "3.141592653589793238462643383279")
    getcontext().prec = 25

    try:
        nums = re.split(r"\+", options)
        result = Decimal(nums[0]) + Decimal(nums[1])
    except:
        pass

    try:
        nums = re.split(r"/", options)
        result = Decimal(nums[0]) / Decimal(nums[1])
    except:
        pass

    try:
        nums = re.split(r"-", options)
        result = Decimal(nums[0]) - Decimal(nums[1])
    except:
        pass

    try:
        nums = re.split(r"\*", options)
        result = Decimal(nums[0]) * Decimal(nums[1])
    except:
        pass

    try:
        nums = re.split(r"%", options)
        result = Decimal(nums[0]) % Decimal(nums[1])
    except:
        pass

    try:
        nums = re.split(r"\*\*", options)
        result = Decimal(nums[0]) ** Decimal(nums[1])
    except:
        pass

    try:
        nums = re.split(r"\^", options)
        result = Decimal(nums[0]) ** Decimal(nums[1])
    except:
        pass

    try:
        # if int(result) == float(result):
        #     result = int(result)
        # else:
        #     result = float(result) 

        bot.reply_to(message, f"`{str(result)}`", parse_mode="Markdown")

        # except Exception as e:
        #     operator = options[1]
        #     num = float(operator.replace("sqrt(", "").replace(")", ""))

        #     if num:
        #         bot.reply_to(message, math.sqrt(num))

        #     if 

    except Exception as e:
        bot.reply_to(message, f"`{e}`", parse_mode="Markdown")

@bot.message_handler(["Math"])
def math_command(message):
    pass

#TODO: REWRITE

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
    try:
        name = message.text.split(maxsplit=1)[1]
    except IndexError:
        bot.reply_to(message, "Напишите название статьи")
        return

    print(f"[Wikipedia {lang.upper()}] {name}")

    page = {}
    wiki = wikipedia.Wikipedia(lang)

    page["orig"] = wiki.page(name)
    if page["orig"].text == "":
        page["orig"] = wiki.page(name.title())
        if page["orig"].text == "":
            page["orig"] = wiki.page(name.upper())
            
    if page["orig"].text == "" and (lang == "ru" or lang == "en" or lang == "uk"):
        #https://speller.yandex.net/services/spellservice.json?op=checkText
        r = requests.get("https://speller.yandex.net/services/spellservice.json/checkText",
                         params={
                             "text": name,
                             "lang": lang
                         })

        data = json.loads(r.text)
        newname = name

        for word in data:
            newname = newname.replace(word["word"], word["s"][0])

        page["orig"] = wiki.page(newname)
        if page["orig"].text == "":
            page["orig"] = wiki.page(newname.title())
            if page["orig"].text == "":
                page["orig"] = wiki.page(newname.upper())



    if page["orig"].text == "":
        bot.reply_to(message, "Не удалось найти статью")
        return

    page["page"] = page["orig"].text
    page["title"] = page["orig"].title
    page["page"] = re.split("\\n", page["page"])[0]

    url = "https://ru.wikipedia.org"
    r = requests.get(url + "/wiki/" + page["title"].replace(" ", "_"))

    page["page"] = page["page"].replace("<", "&lt;").replace(">", "&gt;")

    if page["page"].find("фамилия. Известные носители:") == -1:

        page["page"] = f'<b>{page["page"].replace("(", "</b>(", 1)}'

        if page["page"].find("</b>") == -1:
            page["page"] = page["page"].replace("—", "</b>—", 1)

        if page["page"].find("</b>") == -1:
            page["page"] = page["page"].replace(", котор", "</b>, котор", 1)

        if page["page"].find("</b>") == -1:
            page["page"] = page["page"].replace("-", "</b>—", 1)

        if page["page"].find("</b>") == -1:
            page["page"] = page["orig"].text.replace("<", "&lt;").replace(">", "&gt;")
            page["page"] = re.sub(r"BRBR(Фамилия|Аббревиатура).{,}BRBR", "", page["orig"].text.replace("\n", "BR")).replace("BR", "\n").replace("== Примечания ==", "")
    else:
        page["page"] = page["orig"].text.replace("<", "&lt;").replace(">", "&gt;")

    soup = BeautifulSoup(r.text, 'lxml')
    #bot.send_photo(message, "https:" + page["image_url"], caption=page["page"], parse_mode="HTML")
    try:
        try:
            try:
                page["image_url"] = soup.find("table", class_="infobox").find("td", class_="plainlist").span.a.img["srcset"].split()[2]
            except:
                page["image_url"] = soup.find("td", class_="infobox-image").span.a.img["srcset"].split()[2]
            #page["page"] = soup.find("div", id="mw-content-text").find("div", class_="mw-parser-output").find_all("p")[0].text

            bot.send_photo(message.chat.id, 
                           "https:" + page["image_url"], 
                           caption=page["page"], 
                           parse_mode="HTML",
                           reply_to_message_id=message.message_id)
            #bot.reply_to(message, "https:" + page["image_url"], caption=page["page"], parse_mode="HTML")
        except:
            try:
                page["image_url"] = soup.find("div", class_="mw-parser-output").find("img", class_="thumbimage").get("srcset").split()[0]
                #print(f"{dir(image)=}")
                #page["page"] = soup.find("div", id="mw-content-text").find("div", class_="mw-parser-output").find_all("p")[0].text

                bot.send_photo(message.chat.id, 
                               "https:" + page["image_url"], 
                               caption=page["page"], 
                               parse_mode="HTML",
                               reply_to_message_id=message.message_id)

            except Exception as e:
                print(e)
                #bot.send_message(message.chat.id, page["page"])
                bot.reply_to(message, page["page"], parse_mode="HTML")
    except Exception as e:
        print(e)
        bot.reply_to(message, f"Такой статьи нет\n<code>{e}</code>", parse_mode="HTML")

# @bot.message_handler(commands=["to_tree_my"])
# def to_tree(message):
#     bot.send_message(message.chat.id, "json\n" + dict_to_tree(json.loads(message.reply_to_message.text)), parse_mode="HTML")

# @bot.message_handler(commands=["to_tree_my_info"])
# def to_tree(message):
#     bot.send_message(message.chat.id, message.reply_to_message)

@bot.message_handler(commands=["github"])
def github(message):
    try:
        url = message.text.split(maxsplit=1)[1]
    except:
        bot.reply_to(message, "Введи название аккаунта")
        return
    try:
        r = requests.get(f"https://api.github.com/users/{url}")
        repos = requests.get(f"https://api.github.com/users/{url}/repos")
        data = json.loads(r.text)
        repos_list = json.loads(repos.text)
        text = f'*{data["name"]}*\nFollowers `{data["followers"]}` Following `{data["following"]}`\n\n__{data["bio"]}__\n\nRepositories:'
        for repo in repos_list:
            print(repo["full_name"])
            text += f'\n[{repo["full_name"]}]({repo["html_url"]})'
        bot.send_photo(message.chat.id, 
                       data["avatar_url"], 
                       caption=text,
                       parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(commands=["lurk"])
def lurk(message):
    try:
        name = message.text.split(maxsplit=1)[1]
    except:
        bot.reply_to(message, "Введите название статьи")
        return

    print(f"[Lurkmore] {name}")

    url = "https://lurkmore.to/"
    r = requests.get(url + "index.php",
                     params={"search": name})

    soup = BeautifulSoup(r.text, 'lxml')

    #print(dir(soup.find("div", id="mw-content-text").find("table")))
    #soup.find("div", id="mw-content-text").find("table").remove()

    div = soup.find(id="mw-content-text")

    for t in div.findAll("table", {"class": "lm-plashka"}):
        t.replace_with("")

    for t in div.findAll("table", {"class": "tpl-quote-tiny"}):
        t.replace_with("")

    try:
        page_text = first if (first := div.find("p").text.strip()) else div.findAll("p", recursive=False)[1].text.strip()
    except:
        bot.reply_to(message, "Не удалось найти статью")
        return

    
    # for tag in soup.find(id="mw-content-text").find_all("p"):
    #     if tag.get("class"):
    #         pass
    #     elif tag.parent.get("class") == ["gallerytext"]:
    #         pass
    #     elif re.search(".", tag.text) is None:
    #         pass
    #     else:
    #         page = tag
    #         break



    # page_text = page.text.replace("<", "&lt;").replace(">", "&gt;")
    # page_text = f'<b>{page_text.replace("(", "</b>(", 1)}'

    # if page_text.find("</b>") == -1:
    #     page = f'{page_text.replace("—", "</b>—", 1)}'
    # if page_text.find("</b>") == -1:
    #     try:
    #         page = soup.find(id="mw-content-text").find("p").text
    #     except:
    #         pass

    #center

    try:
        try:
            path = f'https:{div.find(id="fullResImage")["src"]}'
        except:
            path = f'https:{div.find("div", class_="thumb").find("img")["src"]}'
    except Exception as e:
        print(e)
        bot.reply_to(message, "Не удалось загрузить статью")
        return

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

# @bot.message_handler(commands=["bashorg"])
# def bashorg(message):
#     num = int(message.text.replace("/bashorg@jDan734_bot ", "").replace("/bashorg ", ""))
#     r = requests.get(f"https://bash.im/quote/{num}")
#     soup = BeautifulSoup(r.text.replace("<br>", "БАН").replace("<br\\>", "БАН"), 'html.parser')

#     print(soup.find("div", class_="quote__body").text.replace('<div class="quote__body">', "").replace("</div>", "").replace("<br\\>", "\n"))

#     soup2 = BeautifulSoup(soup.find("div", class_="quote__body"), "lxml")
#     bot.reply_to(message, soup2)

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

    #print(r.text)

    soup = BeautifulSoup(r.text, 'lxml')

    if soup.find("div", class_="searchresults") == None:
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


    #print(dir(soup.find("div", id="mw-content-text").find("table")))
    #soup.find("div", id="mw-content-text").find("table").remove()

    div = soup.find(id="mw-content-text")

    for t in div.findAll("table", {"class": "lm-plashka"}):
        t.replace_with("")

    for t in div.findAll("table", {"class": "tpl-quote-tiny"}):
        t.replace_with("")

    try:
        page_text = first if (first := div.find("p").text.strip()) else div.findAll("p", recursive=False)[1].text.strip()
    except Exception as e:
        bot.reply_to(message, "Не удалось найти статью")
        #bot.reply_to(message, e)
        return

    try:
        try:
            path = f'{url}{div.find(id="fullResImage")["src"]}'
        except:
            path = f'{url}{div.find("a", class_="image").find("img")["src"]}'
    except Exception as e:
        # print(e)
        # bot.reply_to(message, "Не удалось загрузить статью")
        # return
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

@bot.message_handler(commands=["to_json"])
def to_json(message):
    bot.send_message(message.chat.id, message.reply_to_message.text.replace("'", "\"").replace("False", "false").replace("True", "true").replace("None", '"none"').replace("<", '"<').replace(">", '>"'))

@bot.message_handler(commands=["sha256"])
def sha(message):
    try:
        if message.reply_to_message.text:
            bot.reply_to(message, hashlib.sha256(bytearray(message.reply_to_message.text.encode("utf-8"))).hexdigest())
        elif message.reply_to_message.document:
            file_id = message.reply_to_message.document.file_id

            document = bot.get_file(file_id)
            bot.reply_to(message, hashlib.sha256(bytearray(bot.download_file(document.file_path))).hexdigest())
        else:
            bot.reply_to(message, hashlib.sha256(bytearray(message.reply_to_message.text.encode("utf-8"))).hexdigest())
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(commands=["sticker_id"])
def get_sticker_id(message):
    print(hasattr("reply_to_message", "message"))
    try:
        bot.reply_to(message, message.reply_to_message.sticker.file_id)
    except Exception as e:
        bot.reply_to(f"Ответь на сообщение со стикером\n`{e}`", parse_mode="Markdown")

@bot.message_handler(commands=["delete"])
def delete(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    try:
        #bot.send_message(message.chat.id, message.reply_to_message)
        print(message.reply_to_message.from_user.id)
        print(message.reply_to_message.message_id)
        if message.reply_to_message.from_user.id == "1121412322":
            bot.delete_message(message.chat.id, message.reply_to_message.message_id)
    except:
        pass

# @bot.message_handler(commands=["delete_message"])
# def delete(message):
#     try:
#         msgid = int(message.text.split(maxsplit=1)[1])
#         bot.delete_message(message.chat.id, msgid)
#         bot.reply_to(message, "Удалил")
#     except:
#         bot.reply_to(message, "Бан))")


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

@bot.message_handler(commands=["xui_pizda"])
def xui_pizda(message):
    stid = choice(["CAACAgIAAx0CUDyGjwACAQ5fCFkeR-pVhI_PUTcTbDGUOgzwfAAC4QADlJlpL9ZRhbtO0tQzGgQ", "CAACAgIAAx0CUDyGjwACAQxfCFkaHE52VvWZzaEDQwUC8FYa-wAC3wADlJlpL5sCLYkiJrDFGgQ"])
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
        true_date = prettyword(number, ["день", "дня", "дней"])

    elif date == "месяцев":
        true_date = prettyword(number, ["месяц", "месяца", "месяцев"])

    elif date == "лет":
        true_date = prettyword(number, ["год", "года", "лет"])


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
    bot.reply_to(message, f'{choice(["Поляк", "Джон", "Александр Гомель", "Иван", "УберКац", "Яблочник", "Электрическая Говноварка"])}?')

@bot.message_handler(content_types=['document', 'video'], func=lambda message: message.chat.id == -1001189395000)
def delete_w10(message):
    try:
        if message.video.file_size == 842295 or message.video.file_size == 912607:
            bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

try:
    bot.polling()
except:
    bot.send_message("795449748", f"`{str(traceback.format_exc())}`", parse_mode="Markdown")
