from aiosqlite import connect

from ..config import settings
from ._migrator import MigratorService
from .chat import Chat, ChatSettings
from .command import Command
from .member import Member
from .note import Note
from .pidor import PidorTop
from .user import User
from .warn import Warn


async def setup_db():
    from pathlib import Path

    async with connect(settings.db_path) as conn:
        await conn.executescript(
            Path("bot/database/_tables.sql").read_text()
        )
        await conn.commit()


__all__ = (
    User,
    Chat,
    ChatSettings,
    Member,
    PidorTop,
    Command,
    Note,
    Warn,
    setup_db,
    MigratorService,
)
