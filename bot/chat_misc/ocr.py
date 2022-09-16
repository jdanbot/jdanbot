import io

import pytesseract
from aiogram import types
from aiogram.dispatcher import filters
from deep_translator import GoogleTranslator as DeepGoogleTranslator
from PIL import Image

from ..config import dp
from ..lib.text import cute_crop


async def photo_to_string(photo: types.PhotoSize, lang: str) -> str | None:
    with io.BytesIO() as file:
        await photo.download(destination_file=file)
        file.seek(0)

        return pytesseract.image_to_string(Image.open(file), lang=lang)


@dp.message_handler(
    filters.RegexpCommandsFilter(regexp_commands=[r"ocr_([a-z]{2,3})2([a-z]{2})"])
)
async def from_ocr(message: types.Message, regexp_command):
    ocr_lang, translate_to_lang = regexp_command.group(1), regexp_command.group(2)

    reply = message.reply_to_message

    if len(ocr_lang) == 2:
        ocr_lang = [
            lang for lang in pytesseract.get_languages() if lang.startswith(ocr_lang)
        ][0]

    text = await photo_to_string(reply.photo[-1], ocr_lang)

    translate_to_lang = translate_to_lang if translate_to_lang != "ua" else "uk"

    t = DeepGoogleTranslator(
        source="auto",
        target=translate_to_lang,
    )
    text = t.translate(text)

    await message.reply(cute_crop(text, limit=4096), disable_web_page_preview=True)


@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=[r"ocr_([a-z]{2,3})"]))
async def from_ocr_to_translated(message: types.Message, regexp_command):
    ocr_lang = regexp_command.group(1)

    reply = message.reply_to_message

    if len(ocr_lang) == 2:
        ocr_lang = [
            lang for lang in pytesseract.get_languages() if lang.startswith(ocr_lang)
        ][0]

    await message.reply(await photo_to_string(reply.photo[-1], ocr_lang))
