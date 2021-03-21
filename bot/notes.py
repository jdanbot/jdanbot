from sqlfocus import SQLTable

from .config import bot, dp, conn
from .lib.text import code, prettyword
from .locale import locale


async def addNote(chatid, name, text):
    try:
        await removeNote(chatid, name)
    except Exception as e:
        print(e)

    table = SQLTable("notes", conn)

    await table.insert(chatid, name, text)
    await conn.commit()


async def getNote(chatid, name):
    table = SQLTable("notes", conn)
    notes = await table.select(where=[f"chatid={chatid}", f'name="{name}"'])

    if len(notes) > 0:
        return notes[-1][-1]
    else:
        return None


async def showNotes(chatid):
    table = SQLTable("notes", conn)
    notes = await table.select(where=[f"chatid={chatid}"])

    return [item[1] for item in notes]


async def removeNote(chatid, name):
    table = SQLTable("notes", conn)
    await table.delete(where=[f"chatid={chatid}", f"name=\"{name}\""])

    await conn.commit()


@dp.message_handler(commands=["remove_note"])
async def cool_secret(message):
    opt = message.text.split(maxsplit=1)

    if len(opt) == 1:
        await message.reply("Введи имя заметки для удаления")

    if opt[1] in locale.adminNotes and message.chat.type == "supergroup":
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

            if note is None:
                return

            try:
                await message.reply(note, parse_mode="MarkdownV2")
            except Exception:
                await message.reply(note)

    else:
        if opt[0] in locale.adminNotes and message.chat.type == "supergroup":
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
