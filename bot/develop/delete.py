from aiogram import types
from ..config import dp


@dp.message_handler(commands="rm", is_superuser=True)
async def rm(message: types.Message):
    await message.reply_to_message.delete()
    await message.delete()
