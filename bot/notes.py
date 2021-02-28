from .lib.prettyword import prettyword
from .config import bot, dp, conn
from .lib.html import code
from .data import data


async def addNote(chatid, name, text):
    try:
        await removeNote(chatid, name)
    except Exception as e:
        print(e)

    sql = 'INSERT INTO notes VALUES ({chatid}, "{name}", "{text}")'

    cur = await conn.cursor()
    await cur.execute(sql.format(chatid=chatid, name=name, text=text))

    await conn.commit()


async def getNote(chatid, name):
    sql = 'SELECT * FROM notes WHERE (chatid={chatid} and name="{name}")'

    cur = await conn.cursor()
    e = await cur.execute(sql.format(chatid=chatid, name=name))
    e = await e.fetchone()

    return e[-1]


async def showNotes(chatid):
    sql = "SELECT * FROM notes WHERE chatid={chatid}".format(chatid=chatid)

    cur = await conn.cursor()
    e = await cur.execute(sql)
    e = await e.fetchall()
    notes = []

    for item in e:
        notes.append(item[1])

    return notes


async def removeNote(chatid, name):
    cur = await conn.cursor()

    sql = 'DELETE FROM notes WHERE (chatid={chatid} and name="{name}")'
    await cur.execute(sql.format(chatid=chatid, name=name))
    await conn.commit()


@dp.message_handler(commands=["remove_note"])
async def cool_secret(message):
    opt = message.text.split(maxsplit=1)

    if len(opt) == 1:
        await message.reply("Введи имя заметки для удаления")

    if opt[1] in data.adminNotes and message.chat.type == "supergroup":
        if await check_admin(message, bot):
            await removeNote(message.chat.id, opt[1])
        else:
            await message.reply("У вас нет прав для изменения этой заметки")
    else:
        await removeNote(message.chat.id, opt[1])


@dp.message_handler(lambda message: message.text.startswith("#"))
async def notes(message):
    opt = message.text.replace("#", "").split(maxsplit=1)
    chatid = message.chat.id

    if len(opt) == 1:
        if opt[0] == "__notes_list__":
            await message.reply(", ".join(showNotes(chatid)))
        else:
            note = await getNote(chatid, opt[0])
            try:
                await message.reply(note, parse_mode="MarkdownV2")
            except Exception:
                await message.reply(note)

    else:
        if opt[0] in data.adminNotes and message.chat.type == "supergroup":
            if await check_admin(message, bot):
                await addNote(chatid, opt[0], opt[1])
                await message.reply("Добавил системную заметку в бд")
            else:
                await message.reply("У вас нет прав для изменения этой заметки")
        else:
            await addNote(chatid, opt[0], opt[1])
            await message.reply("Добавил заметку в бд")


async def check_admin(message, bot):
    chatid = message.chat.id
    userid = message.from_user.id

    user = await bot.get_chat_member(chatid, userid)

    return user.status == "creator" or user.status == "administrator"
