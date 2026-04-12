from aiogram import types
from aiogram.filters import Command, CommandObject
from aiogram.utils.markdown import hcode

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
from ..lib.text import cute_crop
from .lib.aiogoogletrans import AioGoogleTranslator

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
    command_parts = command.command[1:].split("2")

    if len(command_parts) == 1:
        command_parts = command_parts[0].split("to")

    flang, slang = (
        command_parts[0],
        command_parts[1:2] or None,
    )

    if slang is None:
        t = AioGoogleTranslator(
            to_lang=Language.from_str(flang).google
        )
    else:
        t = AioGoogleTranslator(
            to_lang=Language.from_str(slang[0]).google,
            from_lang=Language.from_str(flang).google,
        )

    translation = await t.translate(query)

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
