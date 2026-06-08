import pytest

from bot.memes.memes import bylo
from tests.mocks import mock


@pytest.mark.skip("rewrite")
@pytest.mark.asyncio
async def test_bylo_handler():
    assert (
        await mock(
            func=bylo,
            command="/bylo",
        )
        == "Было"
    )
