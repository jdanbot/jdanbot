from aiogram import types
from .. import handlers
from ..config import dp


@dp.message_handler(commands="rm")
@handlers.only_jdan
async def rm(message: types.Message):
    await message.reply_to_message.delete()
    await message.delete()
