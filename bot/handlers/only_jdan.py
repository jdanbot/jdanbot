from ..config import settings


def only_jdan(func):
    async def wrapper(message):
        if message.from_user.id in settings.bot_owners:
            await func(message)

    return wrapper
