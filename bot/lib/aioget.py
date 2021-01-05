import aiohttp


async def aioget(url, params={}):
    async with aiohttp.ClientSession() as session:
        try:
            response = await session.get(url, params=params)
        except aiohttp.client_exceptions.InvalidURL:
            response = await session.get(f"https://{url}", params=params)

        return response
