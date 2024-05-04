from piccolo.engine.sqlite import SQLiteEngine
from piccolo.table import create_db_tables

DB = SQLiteEngine(path="jdanbot_next.db", log_queries=False)


async def init_db():
    from . import (
        Chat,
        ChatPidor,
        Command,
        Member,
        Note,
        Pidor,
        PidorEvent,
        User,
        Warn,
    )

    await create_db_tables(
        Chat,
        ChatPidor,
        Command,
        Member,
        Pidor,
        PidorEvent,
        User,
        Note,
        Warn,
        if_not_exists=True,
    )
