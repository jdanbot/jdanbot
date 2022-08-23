import pytest

from ..mocks import MessageMock
from bot.develop.calc import eban


@pytest.mark.asyncio
async def test_calc_handler():
    await eban(message_mock := MessageMock(text="/calc 5+5"))
    assert message_mock.replies[0].text == "10"
