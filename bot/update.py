from .bot import dp
import os


@dp.message_handler(lambda message: message.from_user.id == 795449748,
                    commands=["update"])
async def update(message):
    await message.reply("Start update")
    os.system("../after_push.sh")
