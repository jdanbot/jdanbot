import pytest

from ..mocks import mock
from bot.develop.eval import supereval


@pytest.mark.skip("rewrite")
@pytest.mark.asyncio
async def test_eval_handler():
    assert (
        await mock(func=supereval, command="/eval 2*2+2")
        == "`6`"
    )
