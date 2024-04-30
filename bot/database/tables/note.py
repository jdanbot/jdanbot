from piccolo.columns import Boolean, ForeignKey, Timestamp, Varchar
from piccolo.table import Table

from .connection import DB
from .telegram import Member


class Note(Table, db=DB):
    name = Varchar()
    text = Varchar()

    is_admin_note = Boolean()

    author = ForeignKey(Member)
    created_at = Timestamp()

    editor = ForeignKey(Member)
    edited_at = Timestamp(default=None, null=True)
