from piccolo.table import Table
from piccolo.columns import ForeignKey, Timestamp, Varchar

from .connection import DB
from .telegram import Member


class Warn(Table, db=DB):
    who_warned = ForeignKey(Member)

    who_warn = ForeignKey(Member)
    reason = Varchar()
    warned_at = Timestamp()

    who_unwarn = ForeignKey(Member, null=True)
    unwarn_reason = Varchar(null=True)
    unwarned_at = Timestamp(null=True)
