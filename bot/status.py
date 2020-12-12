from .bot import dp, heroku, start_time
from datetime import datetime
from aiogram.utils.markdown import code

import psutil

status = """status
├─heroku: {heroku}
├─memoru:
│ ├─stats: {total}/{used}
│ └─percent: {mem_perc}%
├─cpu: {cpu}%
└─uptime: {uptime}
"""


def to_gb(bytes):
    return int(bytes * 0.00000001) * 0.1


@dp.message_handler(commands=["status"])
async def get_status(message):
    uptime = str(datetime.now() - start_time)
    main = uptime.split(".")[0].split(":")

    h = main[0]
    h = "0" + h if len(h) == 1 else h

    uptime = f"{h}:{main[1]}:{main[2]}"
    mem = psutil.virtual_memory()
    cpu = psutil.cpu_percent()

    text = status.format(total=to_gb(mem.total), uptime=uptime, cpu=cpu,
                         used=to_gb(mem.used), mem_perc=int(mem.percent),
                         heroku=heroku)

    text = code(text).replace("False", "❌") \
                     .replace("True", "✅") \
                     .replace("\\", "")

    await message.reply(text, parse_mode="Markdown")
