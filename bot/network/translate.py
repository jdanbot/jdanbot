from googletrans import Translator
from ..config import dp, bot, _

t = Translator()


async def getTranslate(message, lang):
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
                await message.reply(_("errors.error"))
                await bot.send_message("795449748", e)
                return
    else:
        await message.reply(_("errors.reply_message"))
        return

    try:
        translated = t.translate(text, dest=lang).text
        if len(translated) >= 4096:
            translated = translated[:4096]
    except Exception as e:
        await bot.send_message("795449748", e)
        translated = e

    await message.reply(translated)


@dp.message_handler(commands=["tru"])
async def tru(message):
    await getTranslate(message, "ru")


@dp.message_handler(commands=["ten"])
async def ten(message):
    await getTranslate(message, "en")


@dp.message_handler(commands=["tuk", "tua"])
async def tua(message):
    await getTranslate(message, "uk")


@dp.message_handler(commands=["tbe", "tby"])
async def tbe(message):
    await getTranslate(message, "be")


@dp.message_handler(commands=["tpl"])
async def tpl(message):
    await getTranslate(message, "pl")


@dp.message_handler(commands=["tde"])
async def tpl(message):
    await getTranslate(message, "de")
