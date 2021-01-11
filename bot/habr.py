from .token import bot
from .lib.habr import Habr


@bot.message_handler(["habr"])
def habr(message):
    options = message.text.split(maxsplit=1)

    if len(options) == 1:
        bot.reply_to(message, "Введи id поста из хабра")
        return

    try:
        id_ = int(options[-1])

    except:
        bot.reply_to(message, "Введи валидный id поста")

    h = Habr()

    try:
        bot.reply_to(message,
                     h.page(id_)[:4096],
                     parse_mode="HTML",
                     disable_web_page_preview=True)

    except Exception as e:
        bot.reply_to(message, e)
