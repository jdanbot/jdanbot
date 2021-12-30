from aiogram import types

import subprocess  # noqa: S404
from datetime import datetime
from sys import platform

import psutil
from aiogram.utils.markdown import code

from ..config import dp, STATUS, START_TIME
from ..lib.convert_bytes import convert_bytes
from ..lib.libtree import make_tree


@dp.message_handler(commands=["status"])
async def get_status(message: types.Message):
    mem = psutil.virtual_memory()
    time = str(datetime.now() - START_TIME)

    status = make_tree({
        "memory": "{used} of {total} ({percent})".format(
            used=convert_bytes(mem.used),
            total=convert_bytes(mem.total),
            percent=f"{mem.percent}%"
        ),
        "cpu": f"{psutil.cpu_percent()}%",
        "uptime": time[:time.find(".")]
    }, f"{STATUS} [{get_current_branch()}] on {platform}")

    await message.reply(code(status).replace("\\", ""), parse_mode="Markdown")


def get_current_branch() -> str:
    git_command = "git rev-parse --abbrev-ref HEAD"
    return subprocess.check_output(git_command.split()).decode("utf-8").strip()
