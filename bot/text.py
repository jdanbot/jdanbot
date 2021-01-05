from .bot import dp


@dp.message_handler(commands=["title"])
async def title(message):
    opt = message.text.split(maxsplit=1)
    if len(opt) == 2:
        text = opt[1]

    elif hasattr(message.reply_to_message, "text"):
        text = message.reply_to_message.text

    else:
        await message.reply("Ответь на сообщение")
        return

    await message.reply(text.title())


@dp.message_handler(commands=["upper"])
async def upper(message):
    opt = message.text.split(maxsplit=1)
    if len(opt) == 2:
        text = opt[1]

    elif hasattr(message.reply_to_message, "text"):
        text = message.reply_to_message.text

    else:
        await message.reply("Ответь на сообщение")
        return

    await message.reply(text.upper())


@dp.message_handler(commands=["lower"])
async def lower(message):
    opt = message.text.split(maxsplit=1)
    if len(opt) == 2:
        text = opt[1]

    elif hasattr(message.reply_to_message, "text"):
        text = message.reply_to_message.text

    else:
        await message.reply("Ответь на сообщение")
        return

    await message.reply(text.lower())


@dp.message_handler(commands=["markdown"])
async def markdown(message):
    opt = message.text.split(maxsplit=1)
    if len(opt) == 2:
        text = opt[1]

    elif hasattr(message.reply_to_message, "text"):
        text = message.reply_to_message.text

    else:
        await message.reply("Ответь на сообщение")
        return

    try:
        await message.reply(text, parse_mode="Markdown")
    except:
        await message.reply("Не удалось отправить markdown")
