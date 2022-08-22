import pytest
from bot.chat_misc import notes

from ..types import MessageMock, user_a


@pytest.mark.asyncio
async def test_get_empty_var_handler():
    message_mock = MessageMock(
        text="/get test"
    )

    await notes.get(message=message_mock)

    assert message_mock.replies[0].text == "Создай переменную с помощью /set"


@pytest.mark.asyncio
async def test_set_handler():
    message_mock = MessageMock(
        text="/set test kanobu",
        from_user=user_a
    )

    await notes.set_(message_mock)

    assert message_mock.replies[0].text == "Добавил заметку в бд"

    await notes.get(message_mock2 := MessageMock("/get test"))
    assert message_mock2.replies[0].text == "kanobu"


@pytest.mark.asyncio
async def test_show_notes_handler():
    message_mock = MessageMock(
        text="/show"
    )

    await notes.show(message_mock)
    assert message_mock.replies[0].text == "test"


@pytest.mark.asyncio
async def test_hashtag_notes_handlers():
    message_mock = MessageMock(
        text="#test update kanobu!!!",
        from_user=user_a
    )

    await notes.use_by_hashtag(message_mock)

    assert message_mock.replies[0].text == "Изменил заметку в бд"

    await notes.use_by_hashtag(message_mock2 := MessageMock("#test"))
    assert message_mock2.replies[0].text == "update kanobu!!!"


@pytest.mark.asyncio
async def test_remove_handler():
    message_mock = MessageMock(
        text="/remove test",
        from_user=user_a
    )

    await notes.remove(message_mock)

    message_mock2 = MessageMock(
        text="/get test"
    )
    await notes.get(message_mock2)

    assert message_mock2.replies[0].text == "Создай переменную с помощью /set"
