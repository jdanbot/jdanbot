from aiogram import types

from deep_translator import GoogleTranslator as DeepGoogleTranslator

import re

from .. import handlers
from ..config import dp
from ..lib.text import cute_crop


LANGS = DeepGoogleTranslator().get_supported_languages(as_dict=True)


def fix_lang(lang: str) -> str:
    return lang.replace("ua", "uk").replace("-", "_")

def unfix_lang(lang: str) -> str:
    l = lang.replace("_", "-").split("-")
    return l[0] if len(l) == 1 else "-".join([l[0], l[1].upper()])


LANGS = DeepGoogleTranslator().get_supported_languages(as_dict=True)
LANG_COMMANDS_TR = [
    *[f"t{LANGS[lang]}" for lang in LANGS],
    *[f"t{LANGS[l1]}2{LANGS[l2]}"  for l2 in LANGS for l1 in LANGS],
    *[f"t{LANGS[l1]}to{LANGS[l2]}" for l2 in LANGS for l1 in LANGS]
]


@dp.message_handler(commands=LANG_COMMANDS_TR)
@handlers.get_text
async def translate(message: types.Message, query: str):
    command = message.get_command().removeprefix("/t").split("2")

    if len(command) == 1:
        command = command[0].split("to")

    flang, slang = fix_lang(command[0]), command[1:2] or None

    if slang is None:
        to_lang, from_lang = flang, "auto"
    else:
        to_lang, from_lang = fix_lang(slang[0]), flang

    t = DeepGoogleTranslator(source=unfix_lang(from_lang), target=unfix_lang(to_lang))

    text = t.translate(query)

    await message.reply(cute_crop(text, limit=4096), disable_web_page_preview=True)


@dp.message_handler(commands=["getlangs", "lang_list"])
async def get_langs(message: types.Message):
    await message.answer(
        "<code>/t[lang_code]\n/t[lang_code]2[lang_code]</code>\n<b>lang_codes:</b>\n\n" +
        "\n".join([f"<code>{fix_lang(LANGS[lang])}</code>: {lang}" for lang in LANGS]),
        parse_mode="HTML"
    )
