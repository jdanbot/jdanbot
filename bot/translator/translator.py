from aiogram import types

from deep_translator import GoogleTranslator as DeepGoogleTranslator

from .. import handlers
from ..config import dp, GTRANSLATE_LANGS
from ..lib.text import cute_crop


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
