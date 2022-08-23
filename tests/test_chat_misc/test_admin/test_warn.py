import pytest

from ...mocks import MessageMock
from ...examples import user_a, user_b
from bot.chat_misc.admin import admin_warn, admin_unwarn


@pytest.mark.asyncio
async def test_warn_handler():
    await admin_warn(
        message_mock := MessageMock(
            "/warn тестовый варн",
            from_user=user_a,
            reply_to_message=MessageMock("I WANT WARN", from_user=user_b),
        )
    )
    assert message_mock.replies[0].text == (
        "*[user testowy](tg://user?id=12345678)* выдал 1\\-й пред *[niebaneny człowiek](tg://user?id=1234)*\n\n"  # noqa
        "🤔 *Причина:* тестовый варн"
    )


@pytest.mark.asyncio
async def test_unwarn_handler():
    await admin_unwarn(
        message_mock := MessageMock(
            "/unwarn",
            from_user=user_a,
            reply_to_message=MessageMock("I WANT UNWARN", from_user=user_b),
        )
    )
    assert message_mock.replies[0].text == (
        "*[user testowy](tg://user?id=12345678)* отменил 1\\-й пред *[niebaneny człowiek](tg://user?id=1234)*\n\n"  # noqa
        "🤔 *Причина:* тестовый варн"
    )
