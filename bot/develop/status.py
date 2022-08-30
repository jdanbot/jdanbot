from aiogram import types

import subprocess  # noqa: S404

import pendulum as pdl
from sys import platform

import humanize

import psutil
import distro
import toml

from ..config import dp, settings, START_TIME, _


with open("pyproject.toml", "r") as f:
    pyproject = toml.loads(f.read())

__version__ = pyproject["tool"]["poetry"]["version"]


def pprint_timedelta(duration: pdl.duration) -> str:
    s = duration.total_seconds()

    days,    remainder = divmod(s,         60*60*24)
    hours,   remainder = divmod(remainder, 60*60)
    minutes, seconds   = divmod(remainder, 60)

    return "{:02}:{:02}:{:02}:{:02}".format(
        int(days),
        int(hours),
        int(minutes),
        int(seconds)
    )


@dp.message_handler(commands=["status"])
async def get_status(message: types.Message):
    mem = psutil.virtual_memory()
    time = pdl.now() - START_TIME

    await message.reply(_(
        "dev.status",
        name=settings.status,
        branch=get_current_branch(),
        platform=distro.id() if platform == "linux" else platform,
        version=__version__,

        memory=humanize.naturalsize(mem.used, binary=True),
        total_memory=humanize.naturalsize(mem.total, binary=True),
        uptime=pprint_timedelta(time)
    ), parse_mode="Markdown")


def get_current_branch() -> str:
    git_command = "git rev-parse --abbrev-ref HEAD"

    return subprocess.check_output(git_command.split()).decode("utf-8").strip()
