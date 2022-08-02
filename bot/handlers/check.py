from ..schemas import Note


def check(var, without_params=False):
    def argument_wrapper(func):
        async def wrapper(message):
            res = Note.get(message.chat.id, var)

            if res is None:
                res = "True"

            if str(res).title() == "True":
                await func(message)

        return wrapper

    return argument_wrapper
