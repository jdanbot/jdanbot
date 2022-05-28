from .connection import db

from .chat import Chat
from .chat_member import ChatMember
from .command import Command
from .feed import Feed
from .note import Note
from .pidor import Pidor
from .poll import Poll
from .user import User
from .warn import Warn


def db_setup() -> None:
    db.connect()
    db.create_tables((
        Chat,
        ChatMember,
        Command,
        Feed,
        Note,
        Pidor,
        Poll,
        User,
        Warn
    ), safe=True)

    db.close()
