from piccolo.columns.column_types import (
    Boolean,
    ForeignKey,
    Integer,
    LazyTableReference,
    Timestamp,
    Varchar,
)
from piccolo.columns.m2m import M2M
from piccolo.table import Table

from .connection import DB

from .patches import BetterTable


class Pidor(BetterTable, Table, db=DB):
    member = Integer()
    count = Integer()
    latest_time = Integer()
    # latest_time = Timestamp(default=None, null=True)
    is_allowed = Boolean(default=True)

    chats: list["Chat"] = M2M(
        LazyTableReference("ChatPidor", module_path=__name__)
    )


class Chat(BetterTable, Table, db=DB):
    username = Varchar(null=True)
    title = Varchar()
    members: list["User"] = M2M(
        LazyTableReference("Member", module_path=__name__)
    )
    pidor = ForeignKey(Pidor)
    pidors: list[Pidor] = M2M(
        LazyTableReference("ChatPidor", module_path=__name__)
    )
    pidor_events: list["PidorEvent"] = M2M(
        LazyTableReference("PidorEvent", module_path=__name__)
    )


class User(BetterTable, Table, db=DB):
    username = Varchar(null=True)
    first_name = Varchar()
    last_name = Varchar(null=True)
    chats: list["Chat"] = M2M(
        LazyTableReference("Member", module_path=__name__)
    )


class Member(BetterTable, Table, db=DB):
    user = ForeignKey(User)
    chat = ForeignKey(Chat)

    pidor = ForeignKey(Pidor, null=True)
    pidor_events: list["PidorEvent"] = M2M(
        LazyTableReference("PidorEvent", module_path=__name__)
    )


class PidorEvent(BetterTable, Table, db=DB):
    pidor = ForeignKey(Member)
    chat = ForeignKey(Chat)

    caused_at = Timestamp()


class ChatPidor(Table, db=DB):
    chat = ForeignKey(Chat)
    pidor = ForeignKey(Pidor)


class Command(Table, db=DB):
    user_id = Integer()
    chat_id = Integer()

    name = Varchar()
    args = Varchar(null=True)

    runned_at = Timestamp()
