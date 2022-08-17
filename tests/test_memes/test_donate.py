import pytest

from ..types import MessageMock
from bot.memes.donate import donate


@pytest.mark.asyncio
async def test_donate_handler():
    message_mock = MessageMock(text="/donate")

    await donate(message=message_mock)

    assert message_mock.replies[0].text == (
        "<b>🇷🇺 UMoney:</b> 5599 0050 8875 2808"
    )
