from aiogram import types

from deep_translator import GoogleTranslator as DeepGoogleTranslator


from fluentogram import TranslatorRunner
from ..filters import GetText
from aiogram.filters import Command, CommandObject
from ..config import router
from ..lib.text import cute_crop
from aiogram.utils.markdown import hcode


def fix_lang(lang: str) -> str:
    return lang.replace("ua", "uk").replace("-", "_")


def unfix_lang(lang: str) -> str:
    l = lang.replace("_", "-").split("-")
    return l[0] if len(l) == 1 else "-".join([l[0], l[1].upper()])


LANGS = DeepGoogleTranslator().get_supported_languages(as_dict=True)
# print(LANGS)
LANG_COMMANDS_TR = [
    *[f"t{LANGS[lang]}" for lang in LANGS],
    *[f"t{LANGS[l1]}2{LANGS[l2]}" for l2 in LANGS for l1 in LANGS],
    *[f"t{LANGS[l1]}to{LANGS[l2]}" for l2 in LANGS for l1 in LANGS],
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
        fix_lang(command_parts[0]),
        command_parts[1:2] or None,
    )

    if slang is None:
        to_lang, from_lang = flang, "auto"
    else:
        to_lang, from_lang = fix_lang(slang[0]), flang

    t = DeepGoogleTranslator(
        source=unfix_lang(from_lang), target=unfix_lang(to_lang)
    )

    text = t.translate(query)

    await message.reply(
        cute_crop(text, limit=4096),
        disable_web_page_preview=True,
        parse_mode=None,
    )


@router.message(Command("getlangs", "lang_list", "langs"))
async def get_langs(message: types.Message):
    await message.answer(
        "<code>/t[lang_code]\n/t[lang_code]2[lang_code]</code>\n<b>lang_codes:</b>\n\n"
        + "\n".join(
            [
                hcode(fix_lang(LANGS[lang])) + ": " + lang
                for lang in LANGS
            ]
        ),
        parse_mode="HTML",
    )
