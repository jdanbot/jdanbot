from aiogram import types
from aiogram.filters import Command

from ..config import router
from ..filters import Check, GetText


@router.message(
    Command("poll"), Check("enable_poll"), GetText()
)
async def kz_poll(message: types.Message, query: str):
    options = ["Да", "Нет", "Воздержусь"]
    is_katz_bots = (
        False and message.chat.id == -1001334412934
    )

    if is_katz_bots:
        options.append("Нет прав")

    await message.answer_poll(
        query, options, is_anonymous=False
    )
    await message.delete()


@router.message(Command("open"))
async def open_poll(message: types.Message):
    reply = message.reply_to_message.poll

    await message.answer_poll(
        reply.question,
        [option.text for option in reply.options],
        is_anonymous=False,
        allows_multiple_answers=reply.allows_multiple_answers,
    )
