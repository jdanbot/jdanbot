import pytest
from bot.chat_misc import pidor

from bot.schemas.chat_member import ChatMember

from ..mocks import MessageMock
from ..examples import user_a


@pytest.mark.asyncio
async def test_regpidor():
    await pidor.find_pidor(message_mock := MessageMock("/pidor", from_user=user_a))
    assert message_mock.replies[0].text == "Ты не в базе. Зарегайся через /pidorreg"

    await pidor.reg_pidor(message_mock := MessageMock("/pidorreg", from_user=user_a))
    assert message_mock.replies[0].text == "Попался в базу, ищи себя в `jdanbot.db`"

    await pidor.reg_pidor(message_mock := MessageMock("/pidorreg", from_user=user_a))
    assert message_mock.replies[0].text == "Ты уже в `jdanbot.db`"


@pytest.mark.asyncio
async def test_pidor():
    await pidor.find_pidor(
        message_mock := MessageMock("/pidor", from_user=user_a),
        ignore_pidor_wait=True
    )
    assert f"@{user_a.username}" in message_mock.replies[-1].text

    a = ChatMember.get_by_message(message_mock)

    assert a.pidor.count == 1

    await pidor.find_pidor(message_mock2 := MessageMock("/pidor", from_user=user_a))
    assert "test" in message_mock2.replies_text[0]
