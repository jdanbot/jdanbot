import pytest

from bot.chat_misc import notes
from bot.config.lib.locales import locales
from tests.mocks import mock


@pytest.mark.skip("rewrite")
@pytest.mark.asyncio
async def test_notes():
    assert (
        await mock(
            func=notes.get,
            command="/get test",
        )
        == locales.ru.notes.create_var
    )

    assert (
        await mock(
            func=notes.set_,
            command="/set test testim",
        )
        == "Добавил заметку в бд"
    )

    assert (
        await mock(
            func=notes.get,
            command="/get test",
        )
        == "testim"
    )
    assert (
        await mock(
            func=notes.set_,
            command="/set test tester",
        )
        == "Изменил заметку в бд"
    )

    assert (
        await mock(
            func=notes.get,
            command="/get test",
        )
        == "tester"
    )
