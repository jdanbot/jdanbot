import pytest

from bot.chat_misc import pidor
from bot.config.lib.locales import locales
from bot.database.member import Member
from tests.examples import user_a
from tests.mocks.message import MessageMock
from tests.mocks import mock


@pytest.mark.asyncio
async def test_pidor_is_not_registered():
    assert (
        await mock(
            func=pidor.find_pidor,
            command="/pidor",
        )
        == locales.ru.pidor.reg
    )


@pytest.mark.asyncio
async def test_reg_pidor_is_works():
    assert (
        await mock(
            func=pidor.reg_pidor,
            command="/pidor",
            from_user=user_a,
        )
        == locales.ru.pidor.in_db
    )


@pytest.mark.asyncio
async def test_reg_pidor_is_works_2():
    assert (
        await mock(
            func=pidor.reg_pidor,
            command="/pidor",
            from_user=user_a,
        )
        == locales.ru.pidor.already_in_db
    )
    return True
    await pidor.reg_pidor(
        message_mock := MessageMock(
            text="/pidorreg",
            from_user=user_a,
        ),
    )
    assert message_mock.answer_text == "Ты уже в `jdanbot.db`"


# @pytest.mark.asyncio
# async def test_pidor():
#    await pidor.find_pidor(
#        message_mock := MessageMock("/pidor", from_user=user_a), ignore_pidor_wait=True
#    )
#    assert f"@{user_a.username}" in message_mock.replies[-1].text
#
#    a: Member = await Member.get_by(message_mock)
#
#    assert a.pidor.count == 1
#
#    await pidor.find_pidor(message_mock2 := MessageMock("/pidor", from_user=user_a))
#    assert "test" in message_mock2.replies_text[0]
