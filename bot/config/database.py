import aiosqlite

import asyncio

from .config import DB_PATH


async def connect_db():
    return await aiosqlite.connect(DB_PATH)


conn = asyncio.run(connect_db())
