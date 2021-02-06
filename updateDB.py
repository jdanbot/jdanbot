import sqlite3

from bot.lib.prettyword import prettyword

conn = sqlite3.connect("jdanbot_bac.db")
cur = conn.cursor()

conn2 = sqlite3.connect("jdandb.db")
cur2 = conn2.cursor()

try:
    cur2.execute("DROP TABLE events")
    cur2.execute("CREATE TABLE events (chatid integer, id integer, name text);")
except:
    pass

e = cur2.execute("select * from events").fetchall()

print(e)


def getPrettyUsersName(num):
    return prettyword(num, ["пользователь",
                            "пользователя",
                            "пользователей"])


def getUniqueUsers(cur4, users, chatid):
    try:
        e = cur.execute("SELECT * FROM " + chatid).fetchall()
        print(e)

        for user in e:
            params = (chatid.replace("c", "").replace("_", "-"), *user)
            params = (int(params[0]), params[1], params[2])
            try:
                params = str(params).replace("Val'fey", "Valfey").replace("'", "\"")
            except:
                params = (int(params[0]), params[1], str(params[1]))
            q = f"INSERT INTO events VALUES {params}"
            cur2.execute(q)

            if user[0] in users:
                pass
            else:
                users.append(user[0])

        currentUsers = e
    except Exception as e:
        print(e)
        currentUsers = []

    return [users, currentUsers]


def calc_all_bot_users():
    users = []

    e = cur.execute("SELECT * FROM sqlite_master;").fetchall()
    for table in e:
        users = getUniqueUsers(cur, users, table[1])[0]

    conn2.commit()


calc_all_bot_users()
