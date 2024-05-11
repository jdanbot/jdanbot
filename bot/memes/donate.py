from aiogram import types
from aiogram.filters import Command
from ..config import dp, router


@router.message(Command("donate"))
async def donate(message: types.Message):
    await message.reply("Where is donations, Karl?",
                        parse_mode="HTML",
                        disable_web_page_preview=True)
