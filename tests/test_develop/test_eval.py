import pytest

from ..mocks import MessageMock
from bot.develop.eval import supereval


@pytest.mark.asyncio
async def test_eval_handler():
    await supereval(message_mock := MessageMock(text="/eval 2*2+2"))
    assert message_mock.replies[0].text == "`6`"
