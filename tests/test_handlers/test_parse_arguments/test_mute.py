import pytest
import pytimeparse
from bot import handlers
from bot.config import _
from bot.lib.models.custom_field import CustomField

from ...mocks import MessageMock


async def simple_ban_func(
    message: MessageMock,
    time: CustomField(pytimeparse.parse, fallback=lambda x: int(x) * 60, default=60),
    reason: CustomField(str, default=lambda: _("ban.reason_not_found")),
):
    await message.reply(time)
    await message.reply(reason)


func_ban = handlers.parse_arguments_new(simple_ban_func)


@pytest.mark.asyncio
async def test_ban_new_style():
    await func_ban(message := MessageMock("/mute 4d5h11s test test"))
    assert message.replies_text == (363611, "test test")


@pytest.mark.asyncio
async def test_ban_old_style():
    await func_ban(message2 := MessageMock("/mute 10000 TEST"))
    assert message2.replies_text == (600000, "TEST")


@pytest.mark.asyncio
async def test_ban_with_default_params():
    await func_ban(message3 := MessageMock("/mute"))
    assert message3.replies_text == (3600, "не указана")
