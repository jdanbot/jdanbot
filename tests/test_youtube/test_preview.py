import pytest

from ..types import MessageMock
from bot.youtube.preview import preview


@pytest.mark.asyncio
async def test_preview_handler():
    message_mock = MessageMock(text="/preview https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    await preview(message=message_mock)

    assert message_mock.replies[0].text == "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"  # noqa
