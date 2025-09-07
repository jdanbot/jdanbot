from aiogram import Bot
from aiogram.enums import ChatMemberStatus


async def check_admin(
    bot: Bot, chat_id: int, user_id: int
) -> bool:
    member = await bot.get_chat_member(chat_id, user_id)

    return member.status in (
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.CREATOR,
    )
