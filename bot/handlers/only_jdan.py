def only_jdan(func):
    async def wrapper(message):
        if message.from_user.id == 795449748:
            await func(message)

    return wrapper
