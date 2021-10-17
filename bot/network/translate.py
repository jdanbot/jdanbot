from ..lib.multitran import GoogleTranslator
from ..config import dp, GTRANSLATE_LANGS
from ..lib import handlers
from ..lib.text import cuteCrop

from random import choice


@dp.message_handler(commands=[f"t{lang}" for lang in GTRANSLATE_LANGS])
@handlers.get_text
async def translate(message, query):
    t = GoogleTranslator()

    if (command := message.get_command()) != "/tua":
        lang = command[2:]
    else:
        lang = "uk"

    text = await t.translate(query, tgt_lang=lang)

    await message.reply(cuteCrop(text, limit=4096),
                        disable_web_page_preview=True)

    await t.close()


@dp.message_handler(commands=["crazy"])
@handlers.get_text
async def crazy_translator(message, text):
    t = GoogleTranslator()

    for _ in range(0, 14):
        lang = choice(GTRANSLATE_LANGS)

        if lang == "ua":
            lang = "uk"

        text = await t.translate(text, tgt_lang=lang)

    await message.reply(await t.translate(text, tgt_lang="ru"),
                        disable_web_page_preview=True)

    await t.close()
