from aiogram import types
from aiogram.filters import Command

from ..config import router
from ..filters import IsSuperuser


@router.message(Command("rm"), IsSuperuser())
async def rm(message: types.Message):
    await message.reply_to_message.delete()
    await message.delete()