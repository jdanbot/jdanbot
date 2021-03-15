from .config import bot, dp, conn
from .locale import locale
from .lib.text import code, prettyword


def getPrettyUsersName(users):
    return prettyword(len(users), locale.users)


@dp.message_handler(commands=["me"])
async def me_info(message):
    msg_template = (
        "*Full name:* {name}\n" +
        "*ID:* `{id}`\n\n" +
        "*Common chats*: `{chats}`\n" +
        "*User status*: {status}"
    )

    cur = await conn.cursor()
    sql = "SELECT * FROM events WHERE id={id}"

    e = await cur.execute(sql.format(
        id=message.from_user.id
    ))

    chats = len(await e.fetchall())
    user = await bot.get_chat_member(
        message.chat.id,
        message.from_user.id
    )

    await message.reply(msg_template.format(
        name=message.from_user.full_name,
        id=message.from_user.id,
        chats=chats,
        status=user.status
    ), parse_mode="Markdown")


@dp.message_handler(lambda message: message.from_user.id == 795449748,
                    commands=["users"])
async def calc_all_bot_users(message):
    users = []
    cur = await conn.cursor()

    sql = "SELECT * FROM events WHERE chatid={chatid}"
    chatUsers = await cur.execute(sql.format(chatid=message.chat.id))
    chatUsers = await chatUsers.fetchall()

    e = await cur.execute("SELECT * FROM events")
    e = await e.fetchall()

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

    cur = await conn.cursor()

    e = await cur.execute(f"{select} events where id={message.from_user.id}")

    if await e.fetchone() is None:
        await cur.execute('INSERT INTO events VALUES ({chatid}, {id}, "{name}")'
                          .format(chatid=message.chat.id,
                                  id=message.from_user.id,
                                  name=message.from_user.full_name))
        await conn.commit()
    else:
        pass
