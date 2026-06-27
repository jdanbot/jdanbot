from sqlite3 import Connection

from msgspec import Struct


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
    _ = conn.execute("select * from users limit 1;")
    print(_.fetchmany())
    # return

    MTable("feeds", conn).drop()
    MTable("events", conn).drop()
    MTable("pidor_stats", conn).drop()

    migrate_chats(conn)
    migrate_members(conn)
    migrate_commands(conn)
    migrate_pidors(conn)
    migrate_notes(conn)
    migrate_settings(conn)
    migrate_warns(conn)
    conn.commit()


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
    M.add_column("is_captcha_passed", "BOOLEAN DEFAULT 0")

    M.rename("members")
    conn.execute(
        "UPDATE members SET is_captcha_passed = null"
    )


def migrate_chats(conn: Connection):
    C = MTable("chats", conn)

    C.add_column("language", "VARCHAR(2)")
    C.add_column("settings", 'JSONB NOT NULL DEFAULT "{}"')
    C.rename_column("pidor_of_day_id", "pidor_id")


def migrate_commands(conn: Connection):
    CMD = MTable("commands", conn)

    CMD.rename_column("command", "name")
    CMD.rename_column("params", "args")
    CMD.add_column("executed_at", "TIMESTAMP")
    conn.execute("""
        UPDATE commands
        SET executed_at = CAST(strftime('%s', when_runned, '-3 hours') AS INTEGER)
    ;  
    """)
    conn.execute("""
        UPDATE commands
        SET executed_at = CASE WHEN executed_at < 0
        THEN 0 ELSE executed_at END;
    """)
    CMD.remove_column("when_runned")


def migrate_pidors(conn: Connection):
    P = MTable("pidors", conn)

    P.rename_column("is_pidor_allowed", "is_allowed")
    P.rename_column("latest_pidor_event", "latest_time")

    P.rename("pidors_old")
    conn.execute("""
        CREATE TABLE pidors AS
        SELECT
            PO.id,
            members.user_id,
            members.chat_id,
            PO.is_allowed,
            PO.latest_time
        FROM pidors_old PO
        JOIN members ON PO.member_id = members.id;
    """)
    P.drop()

    E = MTable("pidor_events", conn)
    E.rename("pe_old")

    conn.execute("""
        CREATE TABLE pidor_events AS
        SELECT
            PE.id,
            pidors.chat_id,
            PE.pidor_id,
            PE.caused_at
        FROM pe_old PE
        JOIN pidors ON PE.pidor_id = pidors.id;
    """)
    E.drop()


def migrate_notes(conn: Connection):
    N = MTable("notes", conn)
    N.rename("notes_old")

    conn.execute("""
        CREATE TABLE notes AS
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

    N = MTable("notes", conn)
    N.add_column("is_locked", "BOOLEAN DEFAULT 0")


def migrate_settings(conn: Connection):
    pass


def migrate_warns(conn: Connection):
    W = MTable("warns", conn)
    W.rename("warns_old")

    conn.execute("""
        CREATE TABLE warns AS
        SELECT
            W.id,
            M1.chat_id,
            M1.user_id as victim_id,
            M2.user_id as warn_admin_id,
            W.reason,
            W.warned_at,
            M3.user_id as unwarn_admin_id,
            W.unwarned_at
        FROM warns_old W
        LEFT JOIN members M1 ON W.who_warned_id = M1.id
        LEFT JOIN members M2 ON W.who_warn_id = M2.id
        LEFT JOIN members M3 ON W.who_unwarn_id = M3.id;
    """)
    W.drop()
