from aiovk.drivers import BaseDriver

import aiohttp


class HttpDriver(BaseDriver):
    def __init__(self, timeout=10, loop=None, session=None):
        super().__init__(timeout, loop)

    async def post_json(self, url, params, timeout=None):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=params, timeout=timeout or self.timeout) as response:
                return response.status, await response.json()

    async def get_bin(self, url, params, timeout=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=params, timeout=timeout or self.timeout) as response:
                return response.status, await response.read()

    async def get_text(self, url, params, timeout=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=params, timeout=timeout or self.timeout) as response:
                return response.status, await response.text(), response.real_url

    async def post_text(self, url, data, timeout=None):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, timeout=timeout or self.timeout) as response:
                return response.status, await response.text(), response.real_url

    async def close(self):
        await self.session.close()
