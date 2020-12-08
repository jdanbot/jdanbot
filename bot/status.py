from .bot import dp, heroku, start_time
from datetime import datetime
from aiogram.utils.markdown import code

status = """status
├─working: True
├─heroku: {heroku}
└─uptime: {uptime}
"""


@dp.message_handler(commands=["status"])
async def get_status(message):
    uptime = str(datetime.now() - start_time)
    main = uptime.split(".")[0].split(":")

    h = main[0]
    h = "0" + h if len(h) == 1 else h

    uptime = f"{h}:{main[1]}:{main[2]}"
    text = status.format(heroku=heroku, uptime=uptime)
    text = text.replace("False", "❌") \
               .replace("True", "✅")

    await message.reply(code(text), parse_mode="Markdown")
