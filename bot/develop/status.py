from aiogram import types

import subprocess  # noqa: S404
from datetime import datetime
from sys import platform

import psutil

from ..config import dp, STATUS, START_TIME, _
from .lib.convert_bytes import convert_bytes


@dp.message_handler(commands=["status"])
async def get_status(message: types.Message):
    mem = psutil.virtual_memory()

    time = datetime.now() - START_TIME

    await message.reply(_(
        "dev.status",
        name=STATUS,
        branch=get_current_branch(),
        platform=platform,

        memory=convert_bytes(mem.used),
        total_memory=convert_bytes(mem.total),

        cpu=psutil.cpu_percent(),
        uptime=str(time).split(".")[0]
    ), parse_mode="Markdown")


def get_current_branch() -> str:
    git_command = "git rev-parse --abbrev-ref HEAD"
    return subprocess.check_output(git_command.split()).decode("utf-8").strip()
