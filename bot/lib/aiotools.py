from typing import AsyncGenerator, Callable


async def unpack(
    gen: AsyncGenerator,
    func: Callable = lambda x: x,
) -> list:
    return [func(x) async for x in gen]
