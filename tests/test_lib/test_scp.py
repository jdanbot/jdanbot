import pytest
from bot.lib.scp import SCP


@pytest.mark.asyncio
async def test_search():
    scp = SCP()
    objects = await scp.search("test")


@pytest.mark.asyncio
async def test_page():
    scp = SCP()
    object = await scp.page("http://scp-ru.wikidot.com/scp-1488")

    print(object)
