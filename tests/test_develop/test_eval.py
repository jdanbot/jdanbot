import pytest

from ..types import MessageMock, UserMock
from bot.develop.eval import supereval


@pytest.mark.asyncio
async def test_eval_handler():
    message_mock = MessageMock(
        text="/eval 2*2+2",
        from_user=UserMock(
            id=795449748
        )
    )

    await supereval(message=message_mock)

    assert message_mock.replies[0].text == "<code>6</code>"
