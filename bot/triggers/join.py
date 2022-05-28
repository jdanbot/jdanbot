from random import choice

from ..config import dp, _
from ..schemas import Note, ChatMember


@dp.message_handler(content_types=["new_chat_members"])
async def john(message):
    chat_id = message.chat.id

    if Note.get(chat_id, "__polish_mode__") == "True":
        ChatMember.get_by_message(message)
        await message.delete()
        return

    welcome = Note.get(chat_id, "__enable_greatings__") == "True" or \
        Note.get(chat_id, "__enable_welcome__") == "True"

    if welcome and message.from_user.id == 795449748:
        trigger = choice(_("triggers.jdan_welcome"))

    elif welcome:
        trigger = choice(_("triggers.welcome"))

    else:
        trigger = None

    if trigger:
        await message.reply(f"{trigger}?")

    rules = Note.get(message.chat.id, "__rules__")

    # TODO: REWRITE: MDv2 => HTML in notes

    if rules is not None:
        try:
            await message.answer(rules, parse_mode="MarkdownV2")
        except Exception:
            await message.answer(rules)

    ChatMember.get_by_message(message)
