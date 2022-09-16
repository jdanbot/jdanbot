from aiogram import Bot


async def check_admin(bot: Bot, chat_id: int, user_id: int) -> bool:
    return (await bot.get_chat_member(chat_id, user_id)).is_chat_admin()
