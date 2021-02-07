from .lib.html import code
from .config import bot, dp
from .data import data
from .lib import chez


@dp.message_handler(commands=["java1"])
async def java_secret(message):
    await bot.send_voice(message.chat.id,
                         open("music/java.ogg", "rb+"),
                         reply_to_message_id=message.message_id)


@dp.message_handler(commands=["cool_music"])
async def cool_secret(message):
    await bot.send_voice(message.chat.id,
                         open("music/music.ogg", "rb+"),
                         reply_to_message_id=message.message_id)


@dp.message_handler(commands=["cum"])
async def cum(message):
    await bot.send_voice(message.chat.id,
                         open("music/cum.ogg", "rb+"),
                         reply_to_message_id=message.message_id)


@dp.message_handler(commands=["lyagushka", "frog"])
async def lyagushka(message):
    await bot.send_voice(message.chat.id,
                         open("music/lyagushka.ogg", "rb+"),
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