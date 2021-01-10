from .bot import dp, conn
from .lib.html import code


@dp.message_handler(commands=["leave_from_every"])
async def leaveFromAll(message):
    select = "SELECT * FROM"
    chatid = str(message.chat.id).replace("-", "_")
    user = {
        "id": message.from_user.id,
        "name": " ".join([message.from_user.first_name,
                          message.from_user.last_name])}

    cur = conn.cursor()

    try:
        e = cur.execute(f"{select} c{chatid} where id={user['id']}")
        if e.fetchone() is None:
            await message.reply("Вы не регистрировались")
        else:
            cur.execute(f"DELETE from c{chatid} where id={user['id']}")
            await message.reply("Вас больше нет в бд)))")
    except Exception as err:
        await message.reply(err)


@dp.message_handler(commands=["every"])
async def testAll(message):
    select = "SELECT * FROM"
    chatid = str(message.chat.id).replace("-", "_")
    user = {
        "id": message.from_user.id,
        "name": " ".join([message.from_user.first_name,
                          message.from_user.last_name])}

    cur = conn.cursor()
    try:
        sql = "CREATE TABLE if not exists c{name} (id integer, name text)"
        cur.execute(sql.format(name=chatid))
    except Exception:
        print(Exception)

    cur = conn.cursor()

    e = cur.execute(f"{select} c{chatid} where id={user['id']}")

    if e.fetchone() is None:
        await message.reply("*звуки включения зондов*")
        cur.execute('INSERT INTO c{chatid} VALUES ({id}, "{name}")'
                    .format(chatid=chatid, **user))
        conn.commit()
    else:
        pass

    e = cur.execute("SELECT * FROM c" + chatid)
    users = []
    for user in e:
        users.append(f"[{user[1]}](tg://user?id={user[0]})")

    await message.reply(", ".join(users),
                        parse_mode="MarkdownV2")
