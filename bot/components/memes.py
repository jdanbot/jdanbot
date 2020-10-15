from .token import bot, heroku
from . import texts


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
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    try:
        bot.send_message(message.chat.id, "Было", reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_message(message.chat.id, "Было")


@bot.message_handler(commands=["ne_bylo"])
def ne_bylo(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    try:
        bot.send_message(message.chat.id, "Не было", reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_message(message.chat.id, "Не было")


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


@bot.message_handler(commands=["rzaka"])
def rzaka(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    try:
        bot.send_message(message.chat.id,
                         texts.rzaka,
                         reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_message(message.chat.id, texts.rzaka)


@bot.message_handler(commands=["rzaka_time"])
def rzaka(message):
    bot.reply_to(message, str(texts.rzaka_time) + " часа")


@bot.message_handler(commands=["rzaka_full"])
def rzaka_full(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    try:
        bot.send_message(message.chat.id,
                         texts.rzaka_full,
                         reply_to_message_id=message.reply_to_message.message_id)
    except AttributeError:
        bot.send_message(message.chat.id, texts.rzaka_full)
