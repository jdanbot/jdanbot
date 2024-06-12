from aiogram import types

from deep_translator import GoogleTranslator as DeepGoogleTranslator


from fluentogram import TranslatorRunner
from ..filters import GetText
from aiogram.filters import Command, CommandObject
from ..config import router
from ..lib.text import cute_crop
from aiogram.utils.markdown import hcode
from ..config.languages import (
    Language,
    GTRANSLATE_LANGS as LANGS,
    GLANGS,
    reverse,
    GOOGLE_LANGUAGES_TO_CODES,
)


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
    _: TranslatorRunner,
):
    command_parts = command.command.removeprefix("t").split("2")

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

    t = DeepGoogleTranslator(source=from_lang, target=to_lang)

    text = t.translate(query)

    await message.reply(
        cute_crop(text, limit=4096),
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
