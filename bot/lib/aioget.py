import aiohttp


async def aioget(url, params={}):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if not response.status == 200:
                return 404

            return await response.text()
