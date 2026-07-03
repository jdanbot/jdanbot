from datetime import datetime

from aiogram import types
from aiogram.filters import Command

from ..config import (
    START_TIME,
    Locale,
    __version__,
    router,
    settings,
)
from ..lib.period import period


@router.message(Command("status"))
async def get_status(message: types.Message, _: Locale):
    interval = period(
        datetime.now() - START_TIME,
        "{d:02}:{h:02}:{m:02}:{s:02}",
    )

    await message.reply(
        _.templates.status(
            name=settings.status,
            version=__version__,
            uptime=interval,
        ),
        parse_mode="Markdown",
    )
