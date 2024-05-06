from aiogram import types

import subprocess  # noqa: S404

import arrow
from datetime import timedelta
from sys import platform

from aiogram.filters import Command

import distro
import toml
import humanize
import psutil

from ..config import settings, START_TIME, router

from fluentogram import TranslatorRunner

with open("pyproject.toml", "r") as f:
    pyproject = toml.loads(f.read())

__version__ = pyproject["tool"]["poetry"]["version"]


def pprint_timedelta(duration: timedelta) -> str:
    s = duration.total_seconds()

    days, remainder = divmod(s, 60 * 60 * 24)
    hours, remainder = divmod(remainder, 60 * 60)
    minutes, seconds = divmod(remainder, 60)  # noqa

    return "{:02}:{:02}:{:02}:{:02}".format(
        int(days), int(hours), int(minutes), int(seconds)
    )


@router.message(Command("status"))
async def get_status(message: types.Message, _: TranslatorRunner):
    time = arrow.now() - START_TIME
    mem = psutil.virtual_memory()

    await message.reply(_.hello(username=message.from_user.username))
    await message.reply(
        _.dev.status(
            name=settings.status,
            platform=distro.id() if platform == "linux" else platform,
            version=__version__,
            memory=humanize.naturalsize(mem.used, binary=True),
            total_memory=humanize.naturalsize(mem.total, binary=True),
            uptime=pprint_timedelta(time),
        ),
        parse_mode="Markdown",
    )


def get_current_branch() -> str:
    git_command = "git rev-parse --abbrev-ref HEAD"

    return (
        subprocess.check_output(git_command.split())
        .decode("utf-8")
        .strip()
    )
