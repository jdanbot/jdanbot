import pytest

from ..types import MessageMock
from bot.translator.translator import translate


@pytest.mark.asyncio
async def test_translate_handler():
    message_mock = MessageMock(text="/tru test")

    await translate(message=message_mock)

    assert message_mock.replies[0].text == "тест"
