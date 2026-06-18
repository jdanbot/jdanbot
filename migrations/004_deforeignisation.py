from sqlite3 import Connection


def migrate(database: Connection):
    _ = database.execute("select * from users limit 1;")
    print(_.fetchmany())
    # migrate_users()
    # migrate_
