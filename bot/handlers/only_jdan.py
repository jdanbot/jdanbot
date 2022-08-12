def only_jdan(func):
    async def wrapper(message):
        if message.from_user.id in (795449748, 12345678):
            await func(message)

    return wrapper
