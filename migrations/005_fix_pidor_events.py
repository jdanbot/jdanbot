from sqlite3 import Connection

from pypika import Query, Table

P2 = Table("pidor_events")
P = Table("pidors")


def migrate(conn: Connection):
    _ = conn.execute(
        Query.from_(P2)
        .select("*")
        .where(P2.pidor_id > 20000)
        .get_sql()
    ).fetchall()

    for event in list(_):
        pidor = conn.execute(
            Query.from_(P)
            .select(P.id)
            .where(P.user_id == event[2])
            .where(P.chat_id == event[1])
            .get_sql()
        ).fetchone()

        conn.execute(
            Query.update(P2)
            .set(P2.pidor_id, pidor[0])
            .where(P2.id == event[0])
            .get_sql()
        )

    conn.commit()
