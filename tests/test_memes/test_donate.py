import pytest

from ..mocks import MessageMock
from bot.memes.donate import donate


@pytest.mark.asyncio
async def test_donate_handler():
    await donate(message_mock := MessageMock(text="/donate"))
    assert message_mock.replies[0].text == "<b>🇷🇺 UMoney:</b> 5599 0050 8875 2808"
