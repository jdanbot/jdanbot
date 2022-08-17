import pytest

from ...types import MessageMock, user_a, user_b
from bot.chat_misc.admin import admin_warn, admin_unwarn


@pytest.mark.asyncio
async def test_warn_handler():
    message_mock = MessageMock(
        text="/warn тестовый варн",
        from_user=user_a,

        reply_to_message=MessageMock(
            text="I WANT WARN",
            from_user=user_b
        )
    )

    await admin_warn(message=message_mock)

    assert message_mock.replies[0].text.strip() == """
*[user testowy](tg://user?id=12345678)* выдал 1\\-й пред *[niebaneny człowiek](tg://user?id=1234)*

🤔 *Причина:* тестовый варн
""".strip()


@pytest.mark.asyncio
async def test_unwarn_handler():
    message_mock = MessageMock(
        text="/unwarn",
        from_user=user_a,

        reply_to_message=MessageMock(
            text="I WANT UNWARN",
            from_user=user_b
        )
    )

    await admin_unwarn(message=message_mock)

    assert message_mock.replies[0].text.strip() == """
*[user testowy](tg://user?id=12345678)* отменил 1\\-й пред *[niebaneny człowiek](tg://user?id=1234)*

🤔 *Причина:* тестовый варн
""".strip()
