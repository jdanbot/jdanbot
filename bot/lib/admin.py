from aiogram import Bot
from aiogram import types


async def check_admin(message: types.Message, bot: Bot) -> bool:
    user = await bot.get_chat_member(message.chat.id, message.from_user.id)
    return user.is_chat_admin()
