import pytest

from ...mocks import MessageMock
from ...examples import user_a, user_b
from ...lib import cut_lines
from bot.chat_misc.admin import admin_mute


@pytest.mark.asyncio
async def test_mute_handler():
    await admin_mute(
        message_mock := MessageMock(
            "/mute 1000m50s test_mute",
            from_user=user_a,
            reply_to_message=MessageMock("I WANT BAN", from_user=user_b),
        )
    )
    assert cut_lines(message_mock.replies[0].text, -2) == (
        "*[user testowy](tg://user?id=12345678)* выдал мут *[niebaneny człowiek](tg://user?id=1234)*\n\n"  # noqa
        "🤔 *Причина:* test\\_mute\n"
        "🕓 *Срок:* 16 часов, 40 минут и 50 секунд"
    )
