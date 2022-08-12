import pytest

from ..types import MessageMock
from bot.memes.memes import bylo


@pytest.mark.asyncio
async def test_bylo_handler():
    message_mock = MessageMock(text="/bylo")

    await bylo(message=message_mock)

    assert message_mock.replies[0].text == "Было"
