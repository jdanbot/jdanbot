import pytest
from bot.wikis.slovnyk import slovnyk

from ..mocks import MessageMock


@pytest.mark.asyncio
async def test_slovnyk_handler():
    await slovnyk(message_mock := MessageMock("/slovnyk гачі"))
    assert (
        message_mock.replies[0].text
        == '<b><a href="https://slovnyk.ua/index.php?swrd=%D0%B3%D0%B0%D1%87%D1%96">Г<i>А</i>ЧІ</a></b>, ів, <i>мн., діал.</i> Штани. <i>Та мої товариші за той час.. Сорочки та гачі поскидали І з веселим криком та сміхами Плюскотали вже у срібних хвилях</i> (Фр., XIII, 1954, 347); <i>Коломия мовчки дивилася, як гуцул у червоних гачах ішов шляхом у глиб смерекових лісів</i> (Кундзич, Пов. і опов., 1951, 21).'  # noqa
    )
