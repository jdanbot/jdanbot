import telebot
import random
import re

rules = """
/ban - отправляет "Бан"
/bylo - отправляет "Было"
/ne_bylo - отправляет "Не было"
/fake - отправляет фото с джонами/поляками
/pizda - отправляет мем "пизда"
/net_pizdy - отправляет мем "нет пизда"
/xui - отправляет мем "хуй" 
"""

with open("./token.txt") as token:
	bot = telebot.TeleBot(token.read())
	
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
def bylo(message):
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
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    try:
        bot.send_photo(message.chat.id, open("images/pizda.jpg", "rb"), reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_photo(message.chat.id, open("images/pizda.jpg", "rb").read())

@bot.message_handler(commands=["net_pizdy"])
def net_pizdy(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    try:
        bot.send_photo(message.chat.id, open("images/net_pizdy.jpg", "rb"), reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_photo(message.chat.id, open("images/net_pizdy.jpg", "rb").read())

@bot.message_handler(commands=["xui"])
def xui(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    try:
        bot.send_photo(message.chat.id, open("images/xui.jpg", "rb"), reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_photo(message.chat.id, open("images/xui.jpg", "rb").read())

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

@bot.message_handler(content_types=['text'])
def detect(message):
    if message.text.find("бойкот") != -1:
        bot.reply_to(message, "Вы запостили информацию о бойкоте, если вы бойкотировали, то к вам приедут с паяльником")

@bot.message_handler(content_types=["new_chat_members"])
def john(message):
    number = random.randint(0, 5)
    if number == 0:
        bot.reply_to(message, "Поляк?")
    elif number == 1:
        bot.reply_to(message, "Джон?")
    elif number == 2:
        bot.reply_to(message, "Александр Гомель?")
    elif number == 3:
        bot.reply_to(message, "Иван?")
    elif number == 4:
        bot.reply_to(message, "УберКац?")
    elif number == 5:
        bot.reply_to(message, "Яблочник?")

bot.polling()