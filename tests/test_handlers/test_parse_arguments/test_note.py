from ...mocks import MessageMock
import pytest
from bot.lib.models.custom_field import CustomField


from bot import handlers


async def simple_note_func(
    message: MessageMock,
    key: CustomField(lambda x: x.removeprefix("#")),
    value: CustomField(str, can_take_from_reply=True),
):
    await message.reply(key)
    await message.reply(value)


func = handlers.parse_arguments_new(simple_note_func)


@pytest.mark.asyncio
async def test_param_parser():
    await func(message := MessageMock("/set #test value test2"))
    assert message.replies_text == ("test", "value test2")


@pytest.mark.asyncio
async def test_reply_param():
    await func(
        message2 := MessageMock(
            "/set cool_text", reply_to_message=MessageMock("Make Kanobu Updated Again!")
        )
    )

    assert message2.replies_text == ("cool_text", "Make Kanobu Updated Again!")


@pytest.mark.asyncio
async def test_none_param():
    try:
        await func(MessageMock("/set cool_text2"))
    except Exception as e:
        print(e)
