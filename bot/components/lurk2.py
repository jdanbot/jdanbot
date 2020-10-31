from .token import bot
from .lib.lurkmore import Lurkmore

lurk = Lurkmore()


@bot.message_handler(commands=["lurk2"])
def getlurk(message, logs=False):
    options = message.text.split()
    if len(options) == 1:
        bot.reply_to(message, "Напишите название статьи")
        return

    s = lurk.opensearch(options[1])

    if len(s) == 0:
        bot.reply_to(message, "Не найдено")
        return

    p = lurk.getPage(s)
    # i = lurk.getImagesList(s)
    bot.reply_to(message, str(lurk.parse(p)))
