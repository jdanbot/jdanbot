from ...mocks import MessageMock
import pytest
from bot.lib.models.custom_field import CustomField


from bot import handlers


@pytest.mark.asyncio
async def test_types():
    async def simple_num_func(
        message: MessageMock,
        num: CustomField(int),
        num2: CustomField(float, default=14.88),
        string: CustomField(str),
    ):
        await message.reply(num)
        await message.reply(num2)
        await message.reply(string)

    func = handlers.parse_arguments_new(simple_num_func)

    await func(message := MessageMock("/test 5 kanobu"))
    assert message.replies_text == (5, 14.88, "kanobu")
