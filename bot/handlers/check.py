from ..schemas.note import Note, str2bool


def check(*keys):
    def argument_wrapper(func):
        async def wrapper(message, *args, **kwargs):
            if all(
                Note.get(message.chat.id, key, default=True, type=str2bool)
                for key in keys
            ):
                await func(message, *args, **kwargs)

        return wrapper

    return argument_wrapper
