from ..lib.html import code
from ..config import bot, dp
from ..data import data
from ..lib import chez


egg_commands = []


for egg in data["eggs"]:
    egg_commands.extend(egg["commands"])


@dp.message_handler(commands=egg_commands)
async def sendEgg(message):
    command = message.text.split()[0][1:]

    for egg in data["eggs"]:
        if command in egg["commands"]:
            audio = egg["audio"]

    await bot.send_voice(message.chat.id,
                         open(f"music/{audio}", "rb+"),
                         reply_to_message_id=message.message_id)


@dp.message_handler(commands=["say"])
async def say(message):
    opt = message.text.split(maxsplit=1)

    if len(opt) == 1:
        await bot.reply("Введите текст для аудио")
        return

    await bot.send_voice(message.chat.id,
                         chez.say(opt[1]),
                         reply_to_message_id=message.message_id)


@dp.message_handler(commands=["0x00001488"])
async def secret_error(message):
    await message.reply(code(data["errors"]["egg_error"]),
                        parse_mode="HTML")
