import pytest

from bot.translator.translator import translate
from tests.mocks import mock


@pytest.mark.skip("rewrite")
@pytest.mark.asyncio
async def test_translate_handler():
    assert (
        await mock(
            func=translate,
            command="/tru test",
        )
        == "тест"
    )
