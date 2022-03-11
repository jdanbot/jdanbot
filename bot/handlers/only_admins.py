from ..config import bot
from ..lib.admin import check_admin


def only_admins(func):
    async def wrapper(message):
        if message.chat.type == "supergroup" and await check_admin(message, bot):
            await func(message)

    return wrapper
