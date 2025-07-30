from sys import platform

import distro
import pendulum as pdl
import toml
from aiogram import types
from aiogram.filters import Command
from fluentogram import TranslatorRunner

from ..config import START_TIME, router, settings


with open("pyproject.toml", "r") as f:
    pyproject = toml.loads(f.read())

__version__ = pyproject["tool"]["poetry"]["version"]


def format_interval(duration: pdl.Interval) -> str:
    return "{:02}:{:02}:{:02}:{:02}".format(
        duration.days,
        duration.hours,
        duration.minutes,
        duration.seconds,
    )


@router.message(Command("status"))
async def get_status(message: types.Message, _: TranslatorRunner):
    interval = pdl.now() - START_TIME
    await message.reply(
        _.dev.status(
            name=settings.status,
            platform=distro.id() if platform == "linux" else platform,
            version=__version__,
            uptime=format_interval(interval),
        ),
        parse_mode="Markdown",
    )
