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


def getPrettyUsersName(users):
    return prettyword(len(users), data["users"])


@dp.message_handler(lambda message: message.from_user.id == 795449748,
                    commands=["calc_all_bot_users"])
async def calc_all_bot_users(message):
    users = []
    cur = conn.cursor()

    sql = "SELECT * FROM events WHERE chatid={chatid}"
    chatUsers = cur.execute(sql.format(chatid=message.chat.id)) \
                   .fetchall()

    e = cur.execute("SELECT * FROM events") \
           .fetchall()

    for user in e:
        if user[1] in users:
            pass
        else:
            users.append(user[1])

    # В этом чяте <num> пользователей
    # Всего <num> пользователей

    text = "В этом чяте {} {}\nВсего {} {}"

    await message.reply(text.format(len(chatUsers), getPrettyUsersName(chatUsers),
                                    len(users), getPrettyUsersName(users)))


async def activateSpy(message):
    select = "SELECT * FROM"

    cur = conn.cursor()

    e = cur.execute(f"{select} c{message.chat.id} where id={message.from_user.id}")

    if e.fetchone() is None:
        cur.execute('INSERT INTO events VALUES ({chatid}, {id}, "{name}")'
                    .format(chatid=message.chat.id,
                            id=message.from_user.id,
                            name=message.from_user.full_name))
        conn.commit()
    else:
        pass
