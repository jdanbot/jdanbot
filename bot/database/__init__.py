from .chat import Chat
from .command import Command
from .member import Member
from .note import Note, str2bool
from .pidor import Pidor, PidorEvent, PidorTop
from .user import User
from .warn import Warn

from tortoise import Tortoise


async def setup_db():
    await Tortoise.init(
        db_url="sqlite://tortoise.db",
        modules={"models": ["bot.database"]},
    )

    await Tortoise.generate_schemas()


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
    setup_db,
)
