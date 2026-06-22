from aiosqlite import connect

from ..config import settings
from ._base import queries
from ._migrator import MigratorService
from .chat import Chat, ChatSettings
from .command import Command
from .member import Member
from .note import Note
from .pidor import PidorTop
from .user import User
from .warn import Warn


async def setup_db():
    async with connect(settings.db_path) as conn:
        await queries.init_tables(conn)
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
