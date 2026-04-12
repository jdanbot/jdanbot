from aiogram import types
from aiogram.filters import Command

from ..config import router
from ..database import ChatSettings
from ..filters import Check, GetText


@router.message(
    Command("poll"),
    Check(ChatSettings.enable_poll),
    GetText(),
)
async def create_poll(
    message: types.Message,
    settings: ChatSettings,
    query: str,
):
    options = ["Да", "Нет", "Воздержусь"]

    if settings.enable_extra_poll_option:
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
