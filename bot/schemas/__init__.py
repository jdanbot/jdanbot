from .connection import db

from .chat import Chat
from .chat_member import ChatMember
from .command import Command
from .note import Note, str2bool
from .pidor import Pidor
from .pidor_event import PidorEvent
from .poll import Poll
from .user import User
from .warn import Warn


def db_setup() -> None:
    db.connect()
    db.create_tables((
        Chat,
        ChatMember,
        Command,
        Note,
        Pidor,
        PidorEvent,
        Poll,
        User,
        Warn
    ), safe=True)

    db.close()
