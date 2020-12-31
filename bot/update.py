from .bot import dp
import os


@dp.message_handler(lambda message: False or
                    message.from_user.id == 795449748 or
                    message.from_user.id == 583264555,
                    commands=["update"])
async def update(message):
    await message.reply("Start update")
    os.system("../after-push.sh")
