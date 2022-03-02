import pytest
from bot.lib.monobank import MonobankApi


@pytest.mark.asyncio
async def test_monobank_get_currencies():
    mono = MonobankApi()

    await mono.get_currencies()
