from sys import platform

import os
import distro
from aiogram import types
from aiogram.filters import Command
from msgspec import toml
from whenever import Instant, TimeDelta
from shellous import sh

from ..config import START_TIME, Locale, router, settings

with open("pyproject.toml", "r") as f:
    pyproject = toml.decode(f.read())


__version__ = pyproject["project"]["version"]


async def get_python_version() -> str:
    return os.environ.get("PYTHON_VERSION") or (
        await sh("python", "--version")
    ).removeprefix("Python")


def format_interval(duration: TimeDelta) -> str:
    hours, minutes, seconds, _ = (
        duration.in_hrs_mins_secs_nanos()
    )
    days, hours = divmod(hours, 24)

    return "{:02}:{:02}:{:02}:{:02}".format(
        days, hours, minutes, seconds
    )


@router.message(Command("status"))
async def get_status(message: types.Message, _: Locale):
    interval = Instant.now() - START_TIME

    await message.reply(
        _.templates.status(
            name=settings.status,
            version=__version__,
            platform=distro.id()
            if platform == "linux"
            else platform,
            uptime=format_interval(interval),
        ),
        parse_mode="markdown",
    )

    await message.reply(
        f"python {await get_python_version()}"
        , parse_mode="markdown"
    )
