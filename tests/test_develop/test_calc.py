import pytest

from bot.develop.calc import eban

from tests.mocks import mock


@pytest.mark.asyncio
async def test_calc_handler():
    assert (
        await mock(func=eban, command="/calc 5+5") == "`10`"
    )
