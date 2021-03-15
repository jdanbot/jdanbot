from art import text2art

from ..config import dp
from ..lib import handlers
from ..lib.text import code


@dp.message_handler(commands=["art"])
@handlers.get_text
async def art(message, text):
    if len(text) > 20:
        message.reply("Ты шизик.")
        return

    art = text2art(text, chr_ignore=True)
    await message.reply(code(art), parse_mode="HTML")
