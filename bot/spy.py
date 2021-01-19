from .lib.prettyword import prettyword
from .bot import dp, conn
from .lib.html import code
from .data import data


@dp.message_handler(commands=["leave_from_every"])
async def leaveFromAll(message):
    try:
        name = " ".join([message.from_user.first_name,
                         message.from_user.last_name])
    except:
        name = message.from_user.first_name

    select = "SELECT * FROM"
    chatid = str(message.chat.id).replace("-", "_")
    user = {
        "id": message.from_user.id,
        "name": name}

    cur = conn.cursor()

    try:
        e = cur.execute(f"{select} c{chatid} where id={user['id']}")
        if e.fetchone() is None:
            await message.reply("Вы не регистрировались")
        else:
            cur.execute(f"DELETE from c{chatid} where id={user['id']}")
            conn.commit()
            await message.reply("Вас больше нет в бд")
    except Exception as err:
        await message.reply(err)


def getUniqueUsers(cur, users, chatid):
    try:
        e = cur.execute("SELECT * FROM c" + chatid).fetchall()

        for user in e:
            if user[0] in users:
                pass
            else:
                users.append(user[0])

        currentUsers = e
    except Exception:
        currentUsers = []

    return [users, currentUsers]


def getPrettyUsersName(num):
    return prettyword(num, data["users"])


@dp.message_handler(lambda message: message.from_user.id == 795449748,
                    commands=["calc_all_bot_users"])
async def calc_all_bot_users(message):
    chatid = str(message.chat.id).replace("-", "_")
    users = []
    cur = conn.cursor()

    chatUsers = getUniqueUsers(cur, [], chatid)[1]

    e = cur.execute("SELECT * FROM sqlite_master;").fetchall()
    for table in e:
        users = getUniqueUsers(cur, users, table[1][1:])[0]

    # В этом чяте <num> пользователей
    # Всего <num> пользователей

    text = "В этом чяте {} {}\nВсего {} {}"

    await message.reply(text.format(len(chatUsers),
                                    getPrettyUsersName(len(chatUsers)),
                                    len(users),
                                    getPrettyUsersName(len(users))))


async def activateSpy(message):
    try:
        name = " ".join([message.from_user.first_name,
                         message.from_user.last_name])
    except:
        name = message.from_user.first_name

    select = "SELECT * FROM"
    chatid = str(message.chat.id).replace("-", "_")
    user = {
        "id": message.from_user.id,
        "name": name}

    cur = conn.cursor()
    try:
        sql = "CREATE TABLE if not exists c{name} (id integer, name text)"
        cur.execute(sql.format(name=chatid))
    except Exception:
        print(Exception)

    cur = conn.cursor()

    e = cur.execute(f"{select} c{chatid} where id={user['id']}")

    if e.fetchone() is None:
        cur.execute('INSERT INTO c{chatid} VALUES ({id}, "{name}")'
                    .format(chatid=chatid, **user))
        conn.commit()
    else:
        pass
