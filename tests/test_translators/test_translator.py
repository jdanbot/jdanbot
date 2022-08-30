import pytest

from ..mocks import MessageMock
from bot.translator.translator import translate


@pytest.mark.asyncio
async def test_translate_handler():
    await translate(message_mock := MessageMock(text="/tru test"))
    assert message_mock.replies[0].text == "тест"
