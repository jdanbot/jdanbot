from .bot import bot, dp


@dp.message_handler(lambda message: message.from_user.id == 795449748,
                    commands=["message"])
def msg(message):
    params = message.text.split(maxsplit=2)
    await bot.send_message(params[1], params[2])


@bot.message_handler(lambda message: message.chat.id == -1001189395000,
                     content_types=['document', 'video'])
def delete_w10(message):
    if message.video.file_size == 842295 or \
       message.video.file_size == 912607:
        await message.delete()


@bot.message_handler(lambda message: (False or
                     message.chat.id == -1001176998310 or
                     message.chat.id == -1001374137898) and
                     message.from_user == 1248462292,
                     content_types=['sticker'])
def delete_misha(message):
    if message.sticker.file_size == 20340 and\
       not message.sticker.is_animated:
        await message.delete()


@bot.message_handler(commands=["sticker_id"])
def get_sticker_id(message):
    await message.reply(message.reply_to_message.sticker.file_id)
