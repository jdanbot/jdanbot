import pytest
from bot.wikis.lib.scp import SCP


@pytest.mark.asyncio
async def test_page():
    scp = SCP()
    object = await scp.page("http://scp-ru.wikidot.com/scp-1488")

    assert (
        object.image == "http://scp-ru.wdfiles.com/local--files/scp-1488/wtfturtle3.jpg"
    )
    assert object.href == "http://scp-ru.wikidot.com/scp-1488"
