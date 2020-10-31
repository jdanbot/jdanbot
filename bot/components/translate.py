from .token import bot
from googletrans import Translator

t = Translator()


def getTranslate(message, lang):
    try:
        try:
            text = message.reply_to_message.__dict__["text"]

        except:
            text = message.reply_to_message.__dict__["caption"]

    except Exception as e:
        bot.reply_to(message, "Ошибка")
        bot.send_message("@jDan734", e)
        return

    bot.reply_to(message, t.translate(text, dest=lang).text[:4096])


@bot.message_handler(commands=["tru"])
def tru(message):
    getTranslate(message, "ru")


@bot.message_handler(commands=["ten"])
def ten(message):
    getTranslate(message, "en")


@bot.message_handler(commands=["tuk", "tua"])
def tua(message):
    getTranslate(message, "uk")
