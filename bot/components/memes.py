from .token import bot, heroku
from .texts import texts


def send_meme(message, text):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    try:
        bot.send_message(message.chat.id, text,
                         reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_message(message.chat.id, text)


memes = {
    "bylo": "Было",
    "ne_bylo": "Не было",
    "rzaka": texts["rzaka"],
    "rzaka_full": texts["rzaka_full"],
    "rzaka_time": f"{texts['rzaka_time']} часов"
}


@bot.message_handler(commands=["bylo"])
def bylo(message):
    send_meme(message, memes["bylo"])


@bot.message_handler(commands=["ne_bylo"])
def ne_bylo(message):
    send_meme(message, memes["ne_bylo"])


@bot.message_handler(commands=["rzaka"])
def rzaka(message):
    send_meme(message, memes["rzaka"])


@bot.message_handler(commands=["rzaka_full"])
def rzaka_full(message):
    send_meme(message, memes["rzaka_full"])


@bot.message_handler(commands=["rzaka_time"])
def rzaka_time(message):
    send_meme(message, memes["rzaka_time"])


@bot.message_handler(commands=["ban"])
def ban(message):
    msg = message.text.replace("/ban@jDan734_bot", "").replace("/ban", "")
    send_meme(message, "Бан" + msg)


@bot.message_handler(commands=["fake"])
def polak(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    path = "bot/images/polak.jpg" if heroku else "../images/polak.jpg"

    try:
        bot.send_photo(message.chat.id, open(path, "rb"),
                       reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_photo(message.chat.id, open(path, "rb").read())
