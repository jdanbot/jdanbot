from .token import bot


@bot.message_handler(["title"])
def title(message):
    if len(message.text.split(maxsplit=1)) == 2:
        text = message.text.split(maxsplit=1)[1]

    elif hasattr(message.reply_to_message, "text"):
        text = message.reply_to_message.text

    else:
        bot.reply_to(message, "Ответь на сообщение")
        return

    bot.reply_to(message, text.title())


@bot.message_handler(["upper"])
def upper(message):
    if len(message.text.split(maxsplit=1)) == 2:
        text = message.text.split(maxsplit=1)[1]

    elif hasattr(message.reply_to_message, "text"):
        text = message.reply_to_message.text

    else:
        bot.reply_to(message, "Ответь на сообщение")
        return

    bot.reply_to(message, text.upper())


@bot.message_handler(["lower"])
def lower(message):
    if len(message.text.split(maxsplit=1)) == 2:
        text = message.text.split(maxsplit=1)[1]

    elif hasattr(message.reply_to_message, "text"):
        text = message.reply_to_message.text

    else:
        bot.reply_to(message, "Ответь на сообщение")
        return

    bot.reply_to(message, text.lower())


@bot.message_handler(["markdown"])
def md(message):
    if len(message.text.split(maxsplit=1)) == 2:
        text = message.text.split(maxsplit=1)[1]

    elif hasattr(message.reply_to_message, "text"):
        text = message.reply_to_message.text

    else:
        bot.reply_to(message, "Ответь на сообщение")
        return

    bot.reply_to(message, text.title())

    try:
        bot.reply_to(message, text, parse_mode="Markdown")

    except:
        bot.reply_to(message, "Невалидный markdown")
