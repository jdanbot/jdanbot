import pytest

from ..mocks import MessageMock
from bot.youtube.preview import preview


@pytest.mark.asyncio
async def test_preview_handler():
    await preview(
        message_mock := MessageMock(
            "/preview https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )
    )
    assert (
        message_mock.replies[0].text
        == "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
    )
