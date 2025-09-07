from sys import platform

import distro
import pendulum as pdl
import toml
from aiogram import types
from aiogram.filters import Command

from ..config import START_TIME, Locale, router, settings

with open("pyproject.toml", "r") as f:
    pyproject = toml.loads(f.read())


__version__ = pyproject["project"]["version"]


def format_interval(duration: pdl.Interval) -> str:
    s = duration.total_seconds()

    days, remainder = divmod(s, 60 * 60 * 24)
    hours, remainder = divmod(remainder, 60 * 60)
    minutes, seconds = divmod(remainder, 60)

    return "{:02}:{:02}:{:02}:{:02}".format(
        int(days), int(hours), int(minutes), int(seconds)
    )


@router.message(Command("status"))
async def get_status(message: types.Message, _: Locale):
    interval = pdl.now() - START_TIME

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
