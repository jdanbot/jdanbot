import pytest

from bot.chat_misc import notes

from ..examples import user_a
from ..mocks import MessageMock


@pytest.mark.asyncio
async def test_get_empty_var_handler():
    await notes.get(message_mock := MessageMock("/get test"))
    assert (
        message_mock.replies[0].text
        == "Создай переменную с помощью /set"
    )


@pytest.mark.asyncio
async def test_set_handler():
    await notes.set_(
        message_mock := MessageMock(
            "/set test kanobu", from_user=user_a
        )
    )
    assert message_mock.replies[0].text == "Добавил заметку в бд"

    await notes.get(message_mock2 := MessageMock("/get test"))
    assert message_mock2.replies[0].text == "kanobu"


@pytest.mark.asyncio
async def test_show_notes_handler():
    await notes.show(
        message_mock := MessageMock(
            "/set test kanobu", from_user=user_a
        )
    )
    assert message_mock.replies[0].text == "test"


@pytest.mark.asyncio
async def test_hashtag_notes_handlers():
    await notes.set_(
        MessageMock(
            "/set #enable_inline_set_note True", from_user=user_a
        )
    )
    await notes.use_by_hashtag(
        message_mock := MessageMock(
            "#test update kanobu!!!", from_user=user_a
        )
    )
    assert message_mock.replies[0].text == "Изменил заметку в бд"

    await notes.use_by_hashtag(message_mock2 := MessageMock("#test"))
    assert message_mock2.replies[0].text == "update kanobu!!!"


@pytest.mark.asyncio
async def test_remove_handler():
    await notes.remove(MessageMock("/remove test", from_user=user_a))

    await notes.get(message_mock := MessageMock("/get test"))
    assert (
        message_mock.replies[0].text
        == "Создай переменную с помощью /set"
    )
    assert (
        message_mock.replies[0].text
        == "Создай переменную с помощью /set"
    )
