import re
import textwrap
from random import choice

from aiogram import types
from deep_translator import GoogleTranslator as DeepGoogleTranslator

from .. import handlers
from ..config import dp, GTRANSLATE_LANGS
from ..config.languages import LANGS, Language
from ..config.i18n import i18n
from .lib.multitran import GoogleTranslator


async def cleared_translate(*args, **kwargs) -> str:
    t = GoogleTranslator()

    source_text = await t.translate(*args, **kwargs)
    await t.close()

    text = re.sub(" +", " ", source_text)
    return textwrap.dedent(text)


def get_lang_emoji_by_name(lang_name: str) -> str:
    return LANGS.get(lang_name, Language(lang_name, lang_name)).emoji


@dp.message_handler(commands=["crazy", "crazy2"])
@handlers.get_text
async def crazy_translator(message: types.Message, text: str):
    msg = await message.reply("⏳")

    user_lang = (
        user_lang
        if (user_lang := await i18n.get_user_locale()) in ("uk", "ru", "en") or "ru"
        else "ru"
    )

    langs = []

    for __ in range(7):
        lang = choice(
            tuple(
                filter(
                    lambda x: x not in langs,
                    GTRANSLATE_LANGS,
                )
            )
        )
        lang = "uk" if lang == "ua" else lang
        langs.append(lang)

        text = await cleared_translate(text, tgt_lang=lang)

    langs.append(user_lang)

    await msg.edit_text(
        DeepGoogleTranslator(
            target=user_lang,
        ).translate(text),
        disable_web_page_preview=True,
    )

    if message.get_command(pure=True).endswith("2"):
        await message.answer("".join(map(get_lang_emoji_by_name, langs)))
