import aiohttp


async def aioget(url, params={}):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url, params=params)

        if not response.status == 200:
            return 404

        return response
