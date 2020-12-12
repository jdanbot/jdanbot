from .token import bot
from googletrans import Translator

t = Translator()


def getTranslate(message, lang):
    opt = message.text.split(maxsplit=1)

    if len(opt) != 1:
        text = opt[1]
    elif message.reply_to_message is not None:
        if message.reply_to_message.text is None:
            text = message.reply_to_message.caption

        elif message.reply_to_message.text is not None:
            try:
                text = message.reply_to_message.text
            except Exception as e:
                bot.reply_to(message, "Ошибка")
                bot.send_message("795449748", e)
                return
    else:
        bot.reply_to(message, "Ответь на сообщение")
        return

    try:
        translated = t.translate(text, dest=lang).text
        if len(translated) >= 4096:
            translated = translated[:4096]
    except Exception as e:
        bot.send_message("795449748", e)
        translated = f"Ошибка при переводе\n{e}"

    bot.reply_to(message, translated)


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
