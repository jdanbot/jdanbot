from ..config import bot, dp


@dp.message_handler(lambda message: message.from_user.id == 795449748,
                    commands=["message"])
async def msg(message):
    params = message.text.split(maxsplit=2)
    await bot.send_message(params[1], params[2])


@dp.message_handler(lambda message: message.chat.id == -1001189395000,
                    content_types=['document', 'video'])
async def delete_w10(message):
    if message.video.file_size == 842295 or \
       message.video.file_size == 912607:
        await message.delete()


@dp.message_handler(lambda message: False or
                    message.chat.id == -1001176998310 or
                    message.chat.id == -1001374137898,
                    content_types=['sticker'])
async def delete_misha(message):
    if message.sticker.file_size == 20340 and\
       not message.sticker.is_animated:
        await message.delete()


@dp.message_handler(commands=["sticker_id"])
async def get_sticker_id(message):
    await message.reply(message.reply_to_message.sticker.file_id)
