import pytest
from ..types import MessageMock
from bot.wikis.slovnyk import slovnyk


@pytest.mark.asyncio
async def test_slovnyk_handler():
    message_mock = MessageMock(text="/slovnyk гачі")

    await slovnyk(message=message_mock)

    assert message_mock.replies[0].text.strip() == '<b><a href="https://slovnyk.ua/index.php?swrd=%D0%B3%D0%B0%D1%87%D1%96">ГАЧІ</a></b>, ів, <i>мн., діал.</i> Штани. <i>Та мої товариші за той час.. Сорочки та гачі поскидали І з веселим криком та сміхами Плюскотали вже у срібних хвилях</i> (Фр., XIII, 1954, 347); <i>Коломия мовчки дивилася, як гуцул у червоних гачах ішов шляхом у глиб смерекових лісів</i> (Кундзич, Пов. і опов., 1951, 21).'  # noqa
