import pytest
from aiogram.utils.markdown import code
from art import text2art

from bot.memes.art import art
from tests.mocks import mock


@pytest.mark.skip("rewrite")
@pytest.mark.asyncio
async def test_bylo_handler():
    assert await mock(
        func=art,
        command="/art test",
    ) == code(text2art("test", chr_ignore=True))
