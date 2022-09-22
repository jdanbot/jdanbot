import re
import textwrap
from random import choice

from aiogram import types
from deep_translator import GoogleTranslator as DeepGoogleTranslator

from .. import handlers
from ..config import dp
from ..config.i18n import i18n
from .lib.multitran import GoogleTranslator


GTRANSLATE_LANGS = DeepGoogleTranslator().get_supported_languages(as_dict=True).values()


async def cleared_translate(*args, **kwargs) -> str:
    t = GoogleTranslator()

    source_text = await t.translate(*args, **kwargs)
    await t.close()

    text = re.sub(" +", " ", source_text)
    return textwrap.dedent(text)


@dp.message_handler(commands=["crazy"])
@handlers.get_text
async def crazy_translator(message: types.Message, text: str):
    msg = await message.reply("⏳")

    user_lang = (
        user_lang
        if (user_lang := await i18n.get_user_locale()) in ("uk", "ru", "en") or "ru"
        else "ru"
    )

    lang = user_lang

    for __ in range(9):
        lang = choice(
            tuple(
                filter(
                    lambda x: x != lang,
                    GTRANSLATE_LANGS,
                )
            )
        )
        lang = "uk" if lang == "ua" else lang

        text = await cleared_translate(text, tgt_lang=lang)

    await msg.edit_text(
        await cleared_translate(
            text,
            tgt_lang=user_lang,
        ),
        disable_web_page_preview=True,
    )
