from .lib.prettyword import prettyword
from .config import dp, conn
from .lib.html import code
from .data import data


def addNote(chatid, name, text):
    try:
        removeNote(chatid, name)
    except Exception as e:
        print(e)

    sql = 'INSERT INTO notes VALUES ({chatid}, "{name}", "{text}")'

    cur = conn.cursor()
    e = cur.execute(sql.format(chatid=chatid, name=name, text=text)).fetchone()
    conn.commit()


def getNote(chatid, name):
    sql = 'SELECT * FROM notes WHERE (chatid={chatid} and name="{name}")'

    cur = conn.cursor()
    e = cur.execute(sql.format(chatid=chatid, name=name)).fetchone()

    return e[-1]


def showNotes(chatid):
    sql = "SELECT * FROM notes WHERE chatid={chatid}".format(chatid=chatid)

    cur = conn.cursor()
    e = cur.execute(sql).fetchall()
    notes = []

    for item in e:
        notes.append(item[1])

    return notes


def removeNote(chatid, name):
    cur = conn.cursor()

    sql = 'DELETE FROM notes WHERE (chatid={chatid} and name="{name}")'
    cur.execute(sql.format(chatid=chatid, name=name))
    conn.commit()


@dp.message_handler(commands=["remove_note"])
async def cool_secret(message):
    opt = message.text.split()

    if len(opt) == 1:
        await message.reply("Введи имя заметки для удаления")

    removeNote(message.chat.id, opt[1])


@dp.message_handler(lambda message: message.text.startswith("#"))
async def notes(message):
    opt = message.text.replace("#", "").split(maxsplit=1)
    chatid = message.chat.id

    try:
        if len(opt) == 1:
            if opt[0] == "__notes_list__":
                await message.reply(", ".join(showNotes(chatid)))
            else:
                await message.reply(getNote(chatid, opt[0]))

        else:
            addNote(chatid, opt[0], opt[1])
            await message.reply("Добавил заметку в бд")
    except:
        pass
