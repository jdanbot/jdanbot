from aiogram import types

from deep_translator import GoogleTranslator as DeepGoogleTranslator

from ..lib.multitran import GoogleTranslator
from ..config import dp, GTRANSLATE_LANGS
from ..lib import handlers
from ..lib.text import cute_crop

from random import choice


@dp.message_handler(commands=[f"t{lang}" for lang in GTRANSLATE_LANGS])
@handlers.get_text
async def translate(message: types.Message, query: str):
    if (command := message.get_command().split("@")[0]) != "/tua":
        lang = command[2:]
    else:
        lang = "uk"

    t = DeepGoogleTranslator(source="auto", target=lang)

    text = t.translate(query, tgt_lang=lang)

    await message.reply(cute_crop(text, limit=4096),
                        disable_web_page_preview=True)


@dp.message_handler(commands=["crazy"])
@handlers.get_text
async def crazy_translator(message: types.Message, text: str):
    t = GoogleTranslator()
    msg = await message.reply("Начал шизовый перевод!")

    lang = None

    for _ in range(0, 9):
        lang = choice(list(filter(lambda x: x not in [lang], GTRANSLATE_LANGS)))

        if lang == "ua":
            lang = "uk"

        text = await t.translate(text, tgt_lang=lang)
        msg = await msg.edit_text(f"Начал шизовый перевод!\n{_ + 1}/10 {lang}")

    await msg.edit_text(await t.translate(text, tgt_lang="ru"),
                        disable_web_page_preview=True)

    await t.close()
