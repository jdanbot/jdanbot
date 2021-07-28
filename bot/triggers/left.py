from random import choice

from ..config import dp, _
from ..database import Note


@dp.message_handler(content_types=["left_chat_member"])
async def left_john(message):
    #REWRITE: Add cool phrases for left

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
        await message.reply(f"{trigger} ушел?")