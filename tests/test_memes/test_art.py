import pytest

from ..mocks import MessageMock
from bot.memes.art import art


@pytest.mark.asyncio
async def test_art_handler():
    await art(message_mock := MessageMock(text="/art test"))

    assert (
        message_mock.replies[0].text
        == "<code> _               _   \n| |_   ___  ___ | |_ \n| __| / _ \\/ __|| __|\n| |_ |  __/\\__ \\| |_ \n \\__| \\___||___/ \\__|\n                     \n</code>"  # noqa
    )
