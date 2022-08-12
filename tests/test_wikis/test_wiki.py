import pytest

from dataclasses import dataclass

from aiogram.utils.markdown import bold

from ..types import MessageMock
from bot.wikis.wiki import wikihandler
from bot.triggers.error import catch_error


@dataclass
class CallbackMock:
    message: MessageMock


@pytest.mark.asyncio
async def test_wikipedia_handler():
    message_mock = MessageMock(text="/w канобу")

    await wikihandler(message=message_mock)

    assert message_mock.replies[0].text == """<a href="https://upload.wikimedia.org/wikipedia/ru/thumb/8/86/Kanobu.ru.PNG/872px-Kanobu.ru.PNG">&#8288;</a><b><a href="https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D0%BD%D0%BE%D0%B1%D1%83">Kanobu.ru</a></b> (<i>Кано́бу</i>, сокр. от «КАмень — НОжницы — БУмага») — русскоязычный информационно-развлекательный веб-сайт о компьютерных играх и других видах развлечений. Принадлежит «Бу-Медиа». Существует с 2007 года. До 2011 года представлял собой блог-платформу для любителей игр с элементами социальной сети, позже превратился в интернет-издание с собственной редакцией."""


@pytest.mark.asyncio
async def test_wikipedia_error_handler():
    message_mock = MessageMock(text="/w rwegewgghehuughergh")

    try:
        await wikihandler(message=message_mock)
    except Exception as e:
        await catch_error(CallbackMock(message_mock), e)

    assert message_mock.replies[0].text == bold("Ничего не найдено")
