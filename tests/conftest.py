# import asyncio
# import pytest
# from bot.database._setup import setup_db
# from tortoise.connection import connections


# @pytest.fixture(scope="session")
# def event_loop():
#     loop = asyncio.get_event_loop()
#     yield loop
#     loop.close()


# @pytest.fixture(scope="session", autouse=True)
# @pytest.mark.asyncio
# async def test():
#     await setup_db()
#     yield
#     await connections.close_all()
