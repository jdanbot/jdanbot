from sqlmodel import SQLModel

from .chat import Chat
from .command import Command
from .engine import engine
from .member import Member
from .note import Note, str2bool
from .pidor import Pidor, PidorEvent, PidorTop
from .user import User
from .warn import Warn


async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


__all__ = (
    User,
    Chat,
    Member,
    Pidor,
    PidorEvent,
    PidorTop,
    Command,
    Note,
    str2bool,
    Warn,
    engine,
    setup_db,
)
