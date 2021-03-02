import aiohttp


async def aioget(url, params={}, timeout=10):
    async with aiohttp.ClientSession() as session:
        try:
            response = await session.get(url, params=params,
                                         timeout=timeout)
        except aiohttp.client_exceptions.InvalidURL:
            response = await session.get(f"https://{url}", params=params,
                                         timeout=timeout)

        return response
