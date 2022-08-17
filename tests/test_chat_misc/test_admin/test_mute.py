import pytest

from ...types import MessageMock, user_a, user_b
from bot.chat_misc.admin import admin_mute


@pytest.mark.asyncio
async def test_mute_handler():
    message_mock = MessageMock(
        text="/mute 1000m50s test_mute",
        from_user=user_a,

        reply_to_message=MessageMock(
            text="I WANT BAN",
            from_user=user_b
        )
    )

    await admin_mute(message=message_mock)

    assert message_mock.replies[0].text.startswith("""
*[user testowy](tg://user?id=12345678)* выдал мут *[niebaneny człowiek](tg://user?id=1234)*

🤔 *Причина:* test\\_mute
🕓 *Срок:* 16 часов, 40 минут и 50 секунд

⛓ *Амнистия:*
""".strip())
