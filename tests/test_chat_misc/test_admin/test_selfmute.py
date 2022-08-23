import pytest

from ...mocks import MessageMock
from ...examples import user_a
from ...lib import cut_lines
from bot.chat_misc.admin import selfmute


@pytest.mark.asyncio
async def test_selfmute_handler():
    await selfmute(message_mock := MessageMock("/selfmute 100s test", from_user=user_a))
    assert cut_lines(message_mock.replies[0].text, -1) == (
        "*[user testowy](tg://user?id=12345678)* самозамутился\n\n"
        "🤔 *Причина:* test\n"
        "🕓 *Срок:* 1 минута и 40 секунд\n"
    )
