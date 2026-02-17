from aiogram import types
from aiogram.filters import Command, CommandObject
from aiogram.utils.markdown import hcode
from msgspec import json

from ..config import router
from ..config.languages import (
    GLANGS,
    GOOGLE_LANGUAGES_TO_CODES,
    Language,
    reverse,
)
from ..config.languages import (
    GTRANSLATE_LANGS as LANGS,
)
from ..filters import GetText
from ..lib.aioget import aioget
from ..lib.text import cute_crop

LANG_COMMANDS_TR = [
    *[f"t{lang}" for lang in LANGS],
    *[f"t{l1}2{l2}" for l2 in LANGS for l1 in LANGS],
    *[f"t{l1}to{l2}" for l2 in LANGS for l1 in LANGS],
]


@router.message(Command(*LANG_COMMANDS_TR), GetText())
async def translate(
    message: types.Message,
    query: str,
    command: CommandObject,
):
    command_parts = command.command.removeprefix("t").split(
        "2"
    )

    if len(command_parts) == 1:
        command_parts = command_parts[0].split("to")

    flang, slang = (
        command_parts[0],
        command_parts[1:2] or None,
    )

    if slang is None:
        to_lang, from_lang = Language(flang).google, "auto"
    else:
        to_lang, from_lang = (
            Language(slang[0]).google,
            Language(flang).google,
        )

    # t = DeepGoogleTranslator(source=from_lang, target=to_lang)

    # text = t.translate(query)
    r, text = await aioget(
        "https://clients5.google.com/translate_a/t",
        client="dict-chrome-ex",
        sl=from_lang,
        tl=to_lang,
        q=query,
    )

    translation= json.decode(text)[0][0]

    await message.reply(
        cute_crop(translation, limit=4096),
        disable_web_page_preview=True,
        parse_mode=None,
    )


@router.message(Command("getlangs", "lang_list", "langs"))
async def get_langs(message: types.Message):
    glangs = reverse(GOOGLE_LANGUAGES_TO_CODES)
    langs = [
        hcode(glangs[lang.google]) + ": " + lang.code
        for lang in GLANGS
    ]

    await message.reply(
        "<blockquote expandable><code>/t[lang_code]\n/t[lang_code]2[lang_code]</code>\n<b>lang_codes:</b>\n\n"
        + "\n".join(sorted(set(langs)))
        + "</blockquote>",
        parse_mode="HTML",
    )
