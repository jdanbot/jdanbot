from .token import bot
from googletrans import Translator

t = Translator()


def getTranslate(message, lang):
    try:
        if "reply_to_message" in message.__dict__:
            if message.reply_to_message.text is None:
                text = message.reply_to_message.caption

            elif message.reply_to_message.text is not None:
                text = message.reply_to_message.text
        else:
            bot.reply_to(message, "Ответь на сообщение")
            return

    except Exception as e:
        bot.reply_to(message, "Ошибка")
        bot.send_message("795449748", e)
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


@bot.message_handler(commands=["tbe", "tby"])
def tbe(message):
    getTranslate(message, "be")


@bot.message_handler(commands=["tpl"])
def tbe(message):
    getTranslate(message, "pl")
