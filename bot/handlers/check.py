from ..database.note import Note, str2bool


def check(*keys):
    def argument_wrapper(func):
        async def wrapper(message):
            if all(
                await Note.get(
                    message.chat.id, key, default=True, type=str2bool
                )
                for key in keys
            ):
                await func(message)

        return wrapper

    return argument_wrapper
