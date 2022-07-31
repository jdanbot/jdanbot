import pytest

from ..types import MessageMock
from bot.memes.art import art


@pytest.mark.asyncio
async def test_art_handler():
    message_mock = MessageMock(text="/art test")    

    await art(message=message_mock)

    assert message_mock.replies[0].text == "<code> _               _   \n| |_   ___  ___ | |_ \n| __| / _ \\/ __|| __|\n| |_ |  __/\\__ \\| |_ \n \\__| \\___||___/ \\__|\n                     \n</code>"
