from pathlib import Path
from sqlite3 import Connection
from typing import Any

from msgspec import Struct, convert, json
from pypika import Field, Query, Table
from pypika.functions import Function

from bot.database.chat import ChatSettings

C = Table("chats")
N = Table("notes")


class JsonSet(Function):
    def __init__(
        self, x: Field | str, path: str, *p, alias=None
    ):
        super(JsonSet, self).__init__(
            "json_set", x, path, *p, alias=alias
        )


class Json(Function):
    def __init__(self, value: Any, alias=None):
        super(Json, self).__init__(
            "json", value, alias=alias
        )


class MTable(Struct):
    name: str
    conn: Connection

    def drop(self):
        self.conn.execute(
            f"DROP TABLE IF EXISTS {self.name};"
        )

    @property
    def alter(self):
        return f"ALTER TABLE {self.name}"

    def add_column(self, column: str, type_: str):
        self.conn.execute(
            f"{self.alter} ADD COLUMN {column} {type_.upper()}"
        )

    def rename_column(self, old: str, new: str):
        self.conn.execute(
            f"{self.alter} RENAME COLUMN {old} TO {new}"
        )

    def remove_column(self, column: str):
        self.conn.execute(
            f"{self.alter} DROP COLUMN {column}"
        )

    def rename(self, new_name: str):
        self.conn.execute(
            f"{self.alter} RENAME TO {new_name}"
        )
        self.name = new_name


def migrate(conn: Connection):
    MTable("feeds", conn).drop()
    MTable("events", conn).drop()
    MTable("pidor_stats", conn).drop()

    for index in [
        "chatmember_chat_id",
        "chatmember_user_id",
        "chatmember_pidor_id",
        "poll_author_id",
    ]:
        conn.execute(f"DROP INDEX IF EXISTS {index}")

    for table in [
        "chats",
        "users",
        "commands",
        "notes",
        "pidors",
        "pidor_events",
        "warns",
    ]:
        MTable(table, conn).rename(table + "_old")

    conn.executescript(
        Path("bot/database/_tables.sql")
        .read_text()
        .replace("IF NOT EXISTS ", "")
    )

    migrate_chats(conn)
    migrate_users(conn)
    migrate_members(conn)
    migrate_commands(conn)
    migrate_pidors(conn)
    migrate_notes(conn)
    migrate_settings(conn)
    migrate_warns(conn)
    conn.commit()
    conn.execute("vacuum;")


def migrate_members(conn: Connection):
    M = MTable("chat_members", conn)

    M.add_column("joined_at", "TIMESTAMP")
    conn.execute("""
        UPDATE chat_members
        SET joined_at = CASE 
            WHEN when_joined IS NOT NULL AND when_joined != '' 
            THEN CAST(strftime('%s', when_joined, '-3 hours') AS INTEGER)
            ELSE 0
        END;  
    """)
    M.remove_column("when_joined")

    conn.execute(
        "INSERT INTO members "
        "SELECT cm.id, cm.chat_id, cm.user_id, cm.pidor_id, cm.joined_at, 0, cm.is_admin FROM chat_members cm "
    )
    conn.execute(
        "UPDATE members SET is_captcha_passed = null"
    )
    conn.execute(
        "CREATE UNIQUE INDEX member_chat_user_id "
        "ON members (chat_id, user_id)"
    )
    M.drop()


def migrate_chats(conn: Connection):
    C = MTable("chats_old", conn)

    C.add_column("language", "VARCHAR(2)")
    C.add_column("settings", 'JSONB NOT NULL DEFAULT "{}"')
    C.rename_column("pidor_of_day_id", "pidor_id")

    conn.execute(
        "INSERT INTO chats "
        "SELECT id, username, title, language, pidor_id, settings FROM chats_old",
    )
    C.drop()


def migrate_users(conn: Connection):
    U = MTable("users_old", conn)

    conn.execute(
        "INSERT INTO users "
        "SELECT id, first_name, last_name, username FROM users_old ",
    )
    U.drop()


def migrate_commands(conn: Connection):
    CMD = MTable("commands_old", conn)
    CMD.add_column("executed_at", "TIMESTAMP")
    conn.execute("""
        UPDATE commands_old
        SET executed_at = CAST(strftime('%s', when_runned, '-3 hours') AS INTEGER)
    ;  
    """)
    conn.execute("""
        UPDATE commands_old
        SET executed_at = CASE WHEN executed_at < 0
        THEN 0 ELSE executed_at END;
    """)
    CMD.remove_column("when_runned")

    CMD.add_column("id", "INTEGER")
    conn.execute("UPDATE commands_old SET id = rowid;")
    conn.execute(
        "INSERT INTO commands "
        "SELECT cmd.id, m.chat_id, m.user_id, command, params, executed_at FROM commands_old cmd "
        "LEFT JOIN members M ON cmd.member_id = M.id;"
    )

    CMD.drop()


def migrate_pidors(conn: Connection):
    P = MTable("pidors_old", conn)

    ## FIX PIDOR DUPLICATES
    dups = conn.execute(
        "select member_id, count(*) from pidors_old group by member_id having count(*) > 1"
    ).fetchall()

    for dup in dups:
        duplicates = conn.execute(
            f"select id, member_id from pidors_old where member_id = {dup[0]}"
        ).fetchall()

        valid_pidor = duplicates[0]
        duplicates = duplicates[1:]

        for duplicate in duplicates:
            PE = Table("pidor_events_old")
            conn.execute(
                Query.update(PE)
                .set(PE.pidor_id, valid_pidor[0])
                .where(PE.pidor_id == duplicate[0])
                .get_sql()
            )
            conn.execute(
                f"delete from pidors_old where id = {duplicate[0]}"
            )
    conn.commit()
    ## END FIX PIDOR DUPLICATES!

    P.rename_column("is_pidor_allowed", "is_allowed")
    P.rename_column("latest_pidor_event", "latest_time")

    conn.execute("""
        INSERT INTO pidors
        SELECT
            PO.id,
            M.chat_id,
            M.user_id,
            PO.is_allowed,
            PO.latest_time
        FROM pidors_old PO
        JOIN members M ON PO.member_id = M.id;
    """)
    P.drop()

    E = MTable("pidor_events_old", conn)
    E.rename("pe_old")

    E.add_column("date", "DATE")
    E.add_column("seconds", "INT")
    conn.execute("""
        UPDATE pe_old
        SET date = CASE 
            WHEN caused_at IS NOT NULL AND caused_at != '' 
            THEN substr(caused_at, 0, 11)
            ELSE "1970-01-01"
        END,
            seconds = CASE
            WHEN caused_at IS NOT NULL AND caused_at != '' 
            THEN (
                strftime("%s", substr(caused_at, 0, 20))
                - strftime("%s", date(substr(caused_at, 0, 11)))
            )
            ELSE 0
        END;
    """)

    conn.execute("""
        INSERT INTO pidor_events
        SELECT
            PE.id,
            pidors.chat_id,
            PE.pidor_id,
            PE.date,
            PE.seconds
        FROM pe_old PE
        JOIN pidors ON PE.pidor_id = pidors.id;
    """)
    E.drop()


def migrate_notes(conn: Connection):
    N = MTable("notes_old", conn)

    conn.execute("""
        INSERT INTO notes
        SELECT
            N.id,
            M1.chat_id,
            N.name,
            N.text,
            M1.user_id as author_id,
            N.created_at,
            M2.user_id as editor_id,
            N.edited_at as updated_at,
            N.is_admin_note
        FROM notes_old N
        LEFT JOIN members M1 ON N.author_id = M1.id
        LEFT JOIN members M2 ON N.editor_id = M2.id;
    """)
    N.drop()


def iterate_note(conn: Connection, note_row, option):
    chat_id, name, value = note_row
    value = value.strip()

    try:
        value = int(value)
    except ValueError:
        pass

    if isinstance(value, str):
        if value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False

    if name == "locked_commands":
        value = value.split(" ")

    if option == ChatSettings.enable_kick_on_join:
        if value == "kanobu":
            value = False

    _ = json.encode(
        convert({option.__name__: value}, ChatSettings)
    )

    if _ == b"{}":
        return

    ___ = list(json.decode(_.decode("utf-8")).items())[0][1]
    final = json.encode(___).decode("utf-8")

    conn.execute(
        Query.update(C)
        .set(
            C.settings,
            JsonSet(
                C.settings,
                f"$.{option.__name__}",
                Json(final),
            ),
        )
        .where(C.id == chat_id)
        .get_sql()
    )


def migrate_lang(conn: Connection):
    note = "__chat_lang__"

    _ = conn.execute(
        Query.from_(N)
        .select("chat_id", "text")
        .where(N.name == note)
        .get_sql()
    )
    for row in _.fetchall():
        chat_id, value = row

        conn.execute(
            Query.update(C)
            .set(C.language, value.strip())
            .where(C.id == chat_id)
            .get_sql()
        )

    conn.execute(
        Query.from_(N)
        .delete()
        .where(N.name == note)
        .get_sql()
    )


def migrate_settings(conn: Connection):
    migrate_lang(conn)

    admin_notes = [
        ("__rules__",),
        # ("__enable_bot__"),
        # ("__ban__",),
        # ("__welcome__",),
        (
            "enable_ban_trigger",
            ChatSettings.enable_triggers,
        ),
        (
            "__enable_response__",
            ChatSettings.enable_triggers,
        ),
        (
            "__enable_greatings__",
            ChatSettings.enable_welcome,
        ),
        ("__enable_welcome__", ChatSettings.enable_welcome),
        # ("__warns_to_ban__", ChatSettings.warns_to_ban),
        ("__chat_lang__",),
        ("__enable_admin__", ChatSettings.enable_admin),
        (
            "__enable_selfmute__",
            ChatSettings.enable_selfmute,
        ),
        # ("__polish_mode__", ChatSettings.enable_kick_on_join),
        ("enable_poll", ChatSettings.enable_poll),
        # (
        #     "enable_twitter_redirect",
        #     ChatSettings.enable_twitter_redirect,
        # ),
        # (
        #     "enable_inline_set_note",
        #     ChatSettings.enable_inline_set_note,
        # ),
        ("locked_commands", ChatSettings.locked_commands),
    ]

    for row in admin_notes:
        if isinstance(row, tuple) and len(row) == 2:
            note, dest = row
        else:
            note, dest = row[0], None

        if dest:
            _ = conn.execute(
                Query.from_(N)
                .select(N.chat_id, N.name, N.text)
                .where(N.name == note)
                .get_sql()
            )
            __ = _.fetchall()
            for row_ in __:
                iterate_note(conn, row_, dest)
        conn.execute(
            Query.from_(N)
            .delete()
            .where(N.name == note)
            .get_sql()
        )


def migrate_warns(conn: Connection):
    W = MTable("warns_old", conn)

    conn.execute("""
        INSERT INTO warns
        SELECT
            W.id,
            M1.chat_id,
            M1.user_id as victim_id,
            M2.user_id as warn_admin_id,
            W.reason,
            W.warned_at,
            M3.user_id as unwarn_admin_id,
            w.unwarn_reason,
            W.unwarned_at
        FROM warns_old W
        LEFT JOIN members M1 ON W.who_warned_id = M1.id
        LEFT JOIN members M2 ON W.who_warn_id = M2.id
        LEFT JOIN members M3 ON W.who_unwarn_id = M3.id;
    """)
    W.drop()
