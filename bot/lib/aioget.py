import aiohttp


async def aioget(url, params={}):
    async with aiohttp.ClientSession() as session:
        try:
            response = await session.get(url, params=params)
        except aiohttp.client_exceptions.InvalidURL:
            response = await session.get(f"https://{url}", params=params)

        if not response.status == 200:
            return 404

        return response
