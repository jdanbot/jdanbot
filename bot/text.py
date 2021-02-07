from .config import dp


async def getText(message):
    opt = message.text.split(maxsplit=1)
    if len(opt) == 2:
        text = opt[1]

    elif hasattr(message.reply_to_message, "text"):
        text = message.reply_to_message.text

    else:
        await message.reply("Ответь на сообщение")
        return

    return text


@dp.message_handler(commands=["title"])
async def title(message):
    text = await getText(message)
    await message.reply(text.title())


@dp.message_handler(commands=["upper"])
async def upper(message):
    text = await getText(message)
    await message.reply(text.upper())


@dp.message_handler(commands=["lower"])
async def lower(message):
    text = await getText(message)
    await message.reply(text.lower())


@dp.message_handler(commands=["markdown"])
async def markdown(message):
    text = await getText(message)

    try:
        await message.reply(text, parse_mode="Markdown")
    except Exception:
        await message.reply("Не удалось отправить markdown")
