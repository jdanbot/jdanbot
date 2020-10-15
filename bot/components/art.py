from .token import bot
from art import text2art


@bot.message_handler(["art"])
def art(message):
    options = message.text.split(maxsplit=1)
    if len(options) == 1:
        bot.reply_to(message, "Введи текст на английском для получения арта")
        return

    try:
        if len(options[1]) > 20:
            bot.reply_to(message, "Ты шизик.")
            return

        art = text2art(options[1], chr_ignore=True).replace("<", "&lt;") \
                                                   .replace(">", "&gt;")
        bot.reply_to(message,
                     f"<code>{art}</code>",
                     parse_mode="HTML")
    except:
        bot.reply_to(message, "Не получилось сделать арт")
