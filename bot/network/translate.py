from aiogram import types

from deep_translator import GoogleTranslator as DeepGoogleTranslator

from ..lib.multitran import GoogleTranslator
from ..config import dp, GTRANSLATE_LANGS, FLAGS_EMOJI, _
from ..config.i18n import i18n
from .. import handlers
from ..lib.text import cute_crop

import re
import textwrap

from random import choice


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


@dp.message_handler(commands=["crazy"])
@handlers.get_text
async def crazy_translator(message: types.Message, text: str):
    msg = await message.reply(_("triggers.crazy_translate_started"))

    print(await i18n.get_user_locale())

    lang = None

    for __ in range(0, 9):
        lang = choice(list(filter(lambda x: x not in [lang], GTRANSLATE_LANGS)))
        lang = "uk" if lang == "ua" else lang

        text = await cleared_translate(text, tgt_lang=lang)

        msg = await msg.edit_text(
            _("triggers.crazy_translate_started") +
            f"\n[{__ + 1}/10] {FLAGS_EMOJI[lang]} {lang}"
        )

    await msg.edit_text(
        await cleared_translate(
            text,
            tgt_lang=user_lang if (user_lang := await i18n.get_user_locale()) in ("uk", "ru", "en") else "ru"
        ),
        disable_web_page_preview=True
    )


async def cleared_translate(*args, **kwargs) -> str:
    t = GoogleTranslator()

    source_text = await t.translate(*args, **kwargs)
    await t.close()

    text = re.sub(" +", " ", source_text)
    return textwrap.dedent(text)
