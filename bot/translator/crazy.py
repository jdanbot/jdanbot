import re
import textwrap

from random import choice

from .lib.multitran import GoogleTranslator
from .. import handlers
from ..config import dp, GTRANSLATE_LANGS, LANGS, _
from ..config.i18n import i18n

from aiogram import types


async def cleared_translate(*args, **kwargs) -> str:
    t = GoogleTranslator()

    source_text = await t.translate(*args, **kwargs)
    await t.close()

    text = re.sub(" +", " ", source_text)
    return textwrap.dedent(text)


@dp.message_handler(commands=["crazy"])
@handlers.get_text
async def crazy_translator(message: types.Message, text: str):
    msg = await message.reply(_("triggers.crazy_translate_started"))
    lang = None

    for __ in range(0, 9):
        lang = choice(list(filter(lambda x: x not in [lang], GTRANSLATE_LANGS)))
        lang = "uk" if lang == "ua" else lang
        text = await cleared_translate(text, tgt_lang=lang)

        lang_info = LANGS[lang.lower()]

        msg = await msg.edit_text(
            _("triggers.crazy_translate_started") +
            f"\n[{__ + 1}/10] {lang_info.emoji} {lang_info.name}"
        )

    await msg.edit_text(
        await cleared_translate(
            text,
            tgt_lang=user_lang if (user_lang := await i18n.get_user_locale()) in ("uk", "ru", "en") else "ru"
        ),
        disable_web_page_preview=True
    )