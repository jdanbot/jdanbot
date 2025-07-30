from aiogram import types
from ..config import dp


@dp.message_handler(commands=["donate"])
async def donate(message: types.Message):
    await message.reply("Where are Donations, Carl?",
                        parse_mode="HTML",
                        disable_web_page_preview=True)
