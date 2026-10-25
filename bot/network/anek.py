from aiogram import types
from aiogram.filters import Command

from ..config import router
from .lib.anekru import Anekru


@router.message(Command("anek", "anekry"))
async def anekru_command(message: types.Message):
    anekru = Anekru()
    anek = await anekru.get_random()

    await message.reply(anek, parse_mode=None)
