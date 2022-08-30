from ..config import bot
from ..lib.admin import check_admin

from aiogram import types


def only_admins(func):
    async def wrapper(message: types.Message):
        try:
            message = message.message
        except Exception:
            pass

        if message.chat.type == "supergroup" and await check_admin(message, bot):
            await func(message)

    return wrapper
