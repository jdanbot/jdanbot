import pytest

from ..mocks import MessageMock
from bot.memes.memes import bylo


@pytest.mark.asyncio
async def test_bylo_handler():
    await bylo(message_mock := MessageMock(text="/bylo"))
    assert message_mock.replies[0].text == "Было"
