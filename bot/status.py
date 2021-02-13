import subprocess

from datetime import datetime
from sys import platform

import psutil

from aiogram.utils.markdown import code
from .config import bot_status, dp, start_time
from .lib.convert_bytes import convert_bytes
from .lib.libtree import make_tree


@dp.message_handler(commands=["status"])
async def get_status(message):
    mem = psutil.virtual_memory()
    cpu = psutil.cpu_percent()
    time = str(datetime.now() - start_time)
    status = make_tree({
        "commit": getCurrentCommit(),
        "status": bot_status,
        "os": platform,
        "memory": {
            "used": convert_bytes(mem.used),
            "total": convert_bytes(mem.total),
            "percent": "{}%".format(mem.percent)
        },
        "cpu": "{}%".format(cpu),
        "uptime": time[:time.find(".")]
    }, "status")

    await message.reply(code(status).replace("\\", ""),
                        parse_mode="Markdown")


def getCurrentCommit():
    git_command = ["git", "rev-parse", "--short", "HEAD"]
    return subprocess.check_output(git_command) \
                     .decode("utf-8") \
                     .replace("\n", "")
