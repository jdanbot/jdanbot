from aiogram import types
from aiogram.filters import Command
from msgspec import Struct, toml
from whenever import Instant, TimeDelta

from ..config import START_TIME, Locale, router, settings

with open("pyproject.toml") as f:

    class PyProject(Struct, frozen=True):
        class Project(Struct, frozen=True):
            version: str

        project: Project

    pyproject = toml.decode(f.read(), type=PyProject)


__version__ = pyproject.project.version


def format_interval(duration: TimeDelta) -> str:
    return "{:02}:{:02}:{:02}:{:02}".format(
        *duration.in_units(
            ["days", "hours", "minutes", "seconds"],
            days_assumed_24h_ok=True,
        ).values()
    )


@router.message(Command("status"))
async def get_status(message: types.Message, _: Locale):
    interval = Instant.now() - START_TIME

    await message.reply(
        _.templates.status(
            name=settings.status,
            version=__version__,
            uptime=format_interval(interval),
        ),
        parse_mode="markdown",
    )
