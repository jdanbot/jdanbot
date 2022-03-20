from random import randint


def randomed_start(func):
    async def wrapper(message):
        if randint(0, 1) == 0:
            await func(message)

    return wrapper
