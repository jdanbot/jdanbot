import io
import re

import aiopytesseract as pytesseract
from aiogram import F, types

from ..config import bot, router
from ..lib.errors import JdanbotError
from ..lib.text import cute_crop
from ..translator.lib.aiogoogletrans import (
    AioGoogleTranslator,
)

COMMAND = r"/(ocr_|o)"
LANG = r"([a-z\+]{2,10})"
DEFAULT_LANG = r"([a-z]{2})"
TO = r"(2|to)"

OCR_REGEX = "".join([COMMAND, LANG])
FULL_OCR_REGEX = "".join([COMMAND, LANG, TO, DEFAULT_LANG])


async def photo_to_string(
    photo: types.PhotoSize, lang: str
) -> str | None:
    with io.BytesIO() as file:
        await bot.download(photo, destination=file)
        file.seek(0)

        return await pytesseract.image_to_string(
            file.read(), lang=lang
        )


async def get_full_tesseract_lang(shortlang: str) -> str:
    return [
        lang
        for lang in await pytesseract.get_languages()
        if lang.startswith(shortlang)
    ][0]


@router.message(
    F.text.regexp(FULL_OCR_REGEX) | F.text.regexp(OCR_REGEX)
)
async def from_ocr(message: types.Message):
    command = message.text.split()[0]

    if match := re.match(FULL_OCR_REGEX, command):
        ocr_lang, to_lang = match.group(2), match.group(4)
    elif match := re.match(OCR_REGEX, command):
        ocr_lang, to_lang = match.group(2), None

    if len(langs := ocr_lang.split("+")):
        ocr_lang = "+".join(
            [await get_full_tesseract_lang(lang) for lang in langs]
        )

    reply = message.reply_to_message
    text = await photo_to_string(reply.photo[-1], ocr_lang)

    if text == "":
        raise JdanbotError("errors.failed_to_recognize")

    if to_lang is None:
        return await message.reply(
            text,
            disable_web_page_preview=True,
            parse_mode=None,
        )

    to_lang = to_lang if to_lang != "ua" else "uk"

    t = AioGoogleTranslator(
        to_lang=to_lang,
    )
    text = await t.translate(text)

    await message.reply(
        cute_crop(text, limit=4096),
        parse_mode=None,
        disable_web_page_preview=True,
    )
