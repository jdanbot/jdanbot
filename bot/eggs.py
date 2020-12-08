from .bot import bot, dp


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
