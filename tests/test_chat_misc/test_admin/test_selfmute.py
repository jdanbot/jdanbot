import pytest

from ...types import MessageMock, user_a
from bot.chat_misc.admin import selfmute


@pytest.mark.asyncio
async def test_selfmute_handler():
    message_mock = MessageMock(
        text="/selfmute 100s test",
        from_user=user_a
    )

    await selfmute(message=message_mock)

    assert message_mock.replies[0].text.startswith("""
*[user testowy](tg://user?id=12345678)* самозамутился

🤔 *Причина:* test
🕓 *Срок:* 1 минута и 40 секунд

⛓ *Амнистия:* 
""".strip())
