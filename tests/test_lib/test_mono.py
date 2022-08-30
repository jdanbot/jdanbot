import pytest
from bot.monobank.lib.monobank import MonobankApi


@pytest.mark.asyncio
async def test_monobank_get_currencies():
    mono = MonobankApi()
    currencies = await mono.get_currencies()

    assert len(currencies) != 0
