from .bot import dp, heroku, start_time
from datetime import datetime
from aiogram.utils.markdown import code


@dp.message_handler(commands=["status"])
async def status(message):
    uptime = str(datetime.now() - start_time)
    main = uptime.split(".")[0].split(":")

    h = main[0]
    h = "0" + h if len(h) == 1 else h

    text =  f"status:\n"
    text += f"├─working: True\n"
    text += f"├─heroku: {heroku}\n"
    text += f"└─uptime: {h}:{main[1]}:{main[2]}\n"

    text = text.replace("False", "❌") \
               .replace("True", "✅")

    await message.reply(code(text), parse_mode="Markdown")
