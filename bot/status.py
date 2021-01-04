from .bot import dp, start_time, bot_status
from datetime import datetime
from aiogram.utils.markdown import code

import subprocess
from sys import platform
import psutil

status = """status
├─commit: {commit}
├─status: {status}
├─os: {os}
├─memory:
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
    git_command = ["git", "rev-parse", "--short", "HEAD"]
    commit = subprocess.check_output(git_command).decode("utf-8") \
                                                 .replace("\n", "")

    h = main[0]
    h = "0" + h if len(h) == 1 else h

    uptime = f"{h}:{main[1]}:{main[2]}"
    mem = psutil.virtual_memory()
    cpu = psutil.cpu_percent()

    # token = "environ" if heroku else "file"
    text = status.format(total=to_gb(mem.total), os=platform, uptime=uptime,
                         used=to_gb(mem.used), mem_perc=int(mem.percent),
                         status=bot_status, cpu=cpu, commit=commit)

    text = code(text).replace("False", "❌") \
                     .replace("True", "✅") \
                     .replace("\\", "")

    await message.reply(text, parse_mode="Markdown")
