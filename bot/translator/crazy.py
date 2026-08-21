import random
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
from ..config.lib.locales import Locale
from ..filters import GetText
from .lib.aiogoogletrans import AioGoogleTranslator
from .lib.multitran import (
    GoogleTranslator as CrazyTranslator,
)


def shuffle(text: str) -> str:
    return " ".join(
        random.sample(words := text.split(), len(words))
    )


def get_lang_emoji_by_name(lang_name: str) -> str:
    return LANGS.get(
        lang_name, TranslationLanguage(lang_name, lang_name)
    ).emoji


def clear_text(source_text: str) -> str:
    text = re.sub(" +", " ", source_text)
    return textwrap.dedent(text)


@router.message(
    Command("crazy", "crazy2", "c", "c2"), GetText()
)
async def crazy_translator(
    message: types.Message,
    query: str,
    command: CommandObject,
    _: Locale,
):
    if message.reply_to_message:
        await message.delete()
        message = message.reply_to_message

    msg = await message.reply("⏳")
    t = CrazyTranslator()

    user_lang = (
        user_lang
        if (user_lang := _.lang) in ("uk", "ru", "en")
        or "ru"
        else "ru"
    )

    langs = []
    text = query[:1000]

    if command.command.endswith("2"):
        text = shuffle(text)

    for __ in range(8):
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

        _text = await t.translate(text, tgt_lang=lang)
        text = clear_text(_text)
    await t.close()

    langs.append(user_lang)

    translation = await AioGoogleTranslator(
        to_lang=user_lang,
    ).translate(text)

    await msg.edit_text(
        translation or "None",
        disable_web_page_preview=True,
        parse_mode=None,
    )
