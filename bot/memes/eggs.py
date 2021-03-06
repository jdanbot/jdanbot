from ..lib.html import code
from ..config import bot, dp
from ..locale import locale
from ..lib import chez, handlers


egg_commands = []


for egg in locale.eggs:
    egg_commands.extend(egg["commands"])


@dp.message_handler(commands=egg_commands)
async def sendEgg(message):
    command = message.text.split()[0][1:]

    for egg in locale.eggs:
        if command in egg["commands"]:
            audio = egg["audio"]

    await bot.send_voice(message.chat.id,
                         open(f"music/{audio}", "rb+"),
                         reply_to_message_id=message.message_id)


@dp.message_handler(commands=["say"])
@handlers.get_text
async def say(message, text):
    await bot.send_voice(message.chat.id,
                         chez.say(text),
                         reply_to_message_id=message.message_id)


@dp.message_handler(commands=["0x00001488"])
async def secret_error(message):
    await message.reply(code(locale.errors.egg_error),
                        parse_mode="HTML")
