from .token import bot
from googletrans import Translator

t = Translator()


def getTranslate(message, lang):
    opt = message.text.split(maxsplit=1)
    if len(message.text.split(maxsplit=1)) == 2:
        text = message.text.split(maxsplit=1)[1]

    elif hasattr(message.reply_to_message, "text"):
        text = message.reply_to_message.text

    elif hasattr(message.reply_to_message, "caption"):
        text = message.reply_to_message.caption

    else:
        bot.reply_to(message, "Ответь на сообщение")
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
