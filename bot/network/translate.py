from googletrans import Translator
from ..config import dp, bot, _, GTRANSLATE_LANGS
from ..lib import handlers

from random import choice

t = Translator()


@dp.message_handler(commands=[f"t{lang}" for lang in GTRANSLATE_LANGS])
@handlers.get_text
async def translate(message, text):
    command = message.text.split(" ", maxsplit=1)[0]
    lang = command[2:] if command != "/tua" else "uk"

    await message.reply(t.translate(text, dest=lang).text[:4096],
                        disable_web_page_preview=True)


@dp.message_handler(commands=["crazy"])
@handlers.get_text
async def crazy_translator(message, text):
    for _ in range(0, 14):
        lang = choice(GTRANSLATE_LANGS)

        if lang == "ua":
            lang = "uk"

        text = t.translate(text, dest=lang).text

    await message.reply(t.translate(text, dest="ru").text,
                        disable_web_page_preview=True)
