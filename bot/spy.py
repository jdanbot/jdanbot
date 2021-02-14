from .config import dp, conn
from .data import data
from .lib.prettyword import prettyword
from .lib.html import code


def getPrettyUsersName(users):
    return prettyword(len(users), data.users)


@dp.message_handler(lambda message: message.from_user.id == 795449748,
                    commands=["users"])
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

    e = cur.execute(f"{select} events where id={message.from_user.id}")

    if e.fetchone() is None:
        cur.execute('INSERT INTO events VALUES ({chatid}, {id}, "{name}")'
                    .format(chatid=message.chat.id,
                            id=message.from_user.id,
                            name=message.from_user.full_name))
        conn.commit()
    else:
        pass
