import pytest
from bot.lib.bash import BashOrg


@pytest.mark.asyncio
async def test_random():
    bash = BashOrg()
    quotes = await bash.random()

    assert len(quotes) == 25


@pytest.mark.asyncio
async def test_quote():
    bash = BashOrg()
    quote = await bash.quote(435470)

    assert quote.id == 435470
    assert quote.time == "02.09.2015 в 12:12"
    assert quote.text == 'Коллега несколько дней назад завела котенка:\n\nxxx: как твой котэ там?\nyyy: иногда сидит на плече и смотрит со мной кино\nxxx: о, такими темпами скоро начнет мяукать: "пиастры! пиастры!"'  # noqa
