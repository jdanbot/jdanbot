import pytest

from ..mocks import MessageMock, CallbackMock
from bot.triggers.menu import menu, callback_worker


@pytest.mark.asyncio
async def test_menu_handler():
    await menu(message_mock := MessageMock("/start"))

    btn_row = message_mock.replies[0].reply_markup.inline_keyboard[0]
    assert (btn_row[0].text, btn_row[1].text) == ("✅ Головна", "💻 Сервіси")

    await callback_worker(CallbackMock(message_mock, "network"))

    btn_row = message_mock.replies[1].reply_markup.inline_keyboard[0]
    assert (btn_row[0].text, btn_row[1].text) == ("🏠 Головна", "✅ Сервіси")

    assert message_mock.replies[0].text != message_mock.replies[1].text
