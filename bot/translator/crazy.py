import re
import textwrap
from random import choice

from aiogram import types
from aiogram.filters import Command, CommandObject

from ..config import router
from ..config.languages import (
    CRAZY_LANGS,
    LANGS,
    TranslationLanguage,
)
from ..config.lib.i18n_middleware import i18nMiddleware
from ..filters import GetText
from .lib.multitran import GoogleTranslator


async def cleared_translate(t: GoogleTranslator, *args, **kwargs) -> str:
    source_text = await t.translate(*args, **kwargs)

    text = re.sub(" +", " ", source_text)
    return textwrap.dedent(text)


def get_lang_emoji_by_name(lang_name: str) -> str:
    return LANGS.get(
        lang_name, TranslationLanguage(lang_name, lang_name)
    ).emoji


@router.message(
    Command("crazy", "crazy2", "c", "c2"), GetText()
)
async def crazy_translator(
    message: types.Message,
    query: str,
    command: CommandObject,
):
    msg = await message.reply("⏳")

    mw = i18nMiddleware()
    t = GoogleTranslator()

    user_lang = (
        user_lang
        if (user_lang := await mw.get_language(message))
        in ("uk", "ru", "en")
        or "ru"
        else "ru"
    )

    langs = []
    text = query

    for __ in range(7):
        lang = choice(
            tuple(
                filter(
                    lambda x: x not in langs,
                    CRAZY_LANGS,
                )
            )
        )
        lang = "uk" if lang == "ua" else lang
        langs.append(lang)

        text = await cleared_translate(t, text, tgt_lang=lang)
    await t.close()

    langs.append(user_lang)

    await msg.edit_text(
        DeepGoogleTranslator(
            target=user_lang,
        ).translate(text)
        or "None",
        disable_web_page_preview=True,
        parse_mode=None,
    )

    if command.command.endswith("2"):
        await message.answer(
            "".join(map(get_lang_emoji_by_name, langs))
        )
