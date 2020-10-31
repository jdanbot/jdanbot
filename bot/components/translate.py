from .token import bot
from googletrans import Translator

t = Translator()


def getTranslate(message, lang):
    opt = message.text.split(maxsplit=1)
    if len(opt) == 1:
        bot.reply_to(message, "Введите текст")
        return

    else:
        text = opt[1]

    return t.translate(text, lang)


@bot.message_handler(commands=["tru"])
def tru(message):
    getTranslate(message, "ru")


@bot.message_handler(commands=["ten"])
def ten(message):
    getTranslate(message, "en")


@bot.message_handler(commands=["tuk", "tua"])
def tua(message):
    getTranslate(message, "ua")
