import pytest

from ..types import MessageMock
from bot.develop.calc import eban


@pytest.mark.asyncio
async def test_art_handler():
    message_mock = MessageMock(text="/calc 5+5")

    await eban(message=message_mock)

    assert message_mock.replies[0].text == "10"
