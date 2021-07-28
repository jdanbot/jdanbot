from random import choice

from ..config import dp, _
from ..database import Note, Event


@dp.message_handler(content_types=["new_chat_members"])
async def john(message):
    chat_id = message.chat.id

    welcome = await Note.get(chat_id, "__enable_greatings__") == "True" or \
              await Note.get(chat_id, "__enable_welcome__")   == "True"

    if welcome and message.from_user.id == 795449748:
        trigger = choice(_("triggers.jdan_welcome"))

    elif welcome:
        trigger = choice(_("triggers.welcome"))
    
    else:
        trigger = None

    if trigger:
        await message.reply(f"{trigger}?")

    rules = await Note.get(message.chat.id, "__rules__")

    #REWRITE: MDv2 => HTML in notes

    if rules is not None:
        try:
            await message.answer(rules, parse_mode="MarkdownV2")
        except Exception:
            await message.answer(rules)

    await Event.reg_user_in_db(message)