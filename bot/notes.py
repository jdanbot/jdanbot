from sqlfocus import SQLTable

from .config import bot, dp, conn, notes
from .lib import handlers
from .lib.admin import check_admin
from .lib.text import code, prettyword
from .locale import locale


async def addNote(chatid, name, text):
    try:
        await removeNote(chatid, name)
    except Exception as e:
        print(e)

    await notes.insert(chatid, name, text)
    await conn.commit()


async def getNote(chatid, name):
    e = await notes.select(where=[f"{chatid = }", f'name="{name}"'])

    if len(e) > 0:
        return e[-1][-1]
    else:
        return None


async def showNotes(chatid):
    e = await notes.select(where=[f"chatid={chatid}"])

    return [item[1] for item in e]


async def removeNote(chatid, name):
    await notes.delete(where=[f"chatid={chatid}", f"name=\"{name}\""])
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


@dp.message_handler(commands=["set"])
@handlers.parse_arguments(3)
async def set_(message, params):
    name = params[1][1:] if params[1].startswith("#") else params[1]

    if name in locale.adminNotes and message.chat.type == "supergroup":
        if await check_admin(message, bot):
            await addNote(message.chat.id, name, params[2])
            await message.reply("Добавил системную заметку в бд")
        else:
            await message.reply("У вас нет прав для изменения этой заметки")
    else:
        await addNote(message.chat.id, name, params[2])
        await message.reply("Добавил заметку в бд")


@dp.message_handler(commands=["get"])
@handlers.parse_arguments(2)
async def get_(message, params):
    name = params[1][1:] if params[1].startswith("#") else params[1]

    if name == "__notes_list__":
        await message.reply(", ".join(await showNotes(message.chat.id)))
        return

    note = await getNote(message.chat.id, name)

    if note is None:
        await message.reply("Создай переменную с помощью /set")
        return

    try:
        await message.reply(note, parse_mode="MarkdownV2")
    except Exception:
        await message.reply(note)


@dp.message_handler(lambda message: message.text.startswith("#"))
async def notes_(message):
    name = message.text.replace("#", "")
    chatid = message.chat.id

    if len(name) <= 50:
        if name == "__notes_list__":
            await message.reply(", ".join(await showNotes(chatid)))
        else:
            note = await getNote(chatid, name)

            if note is None:
                return

            try:
                await message.reply(note, parse_mode="MarkdownV2")
            except Exception:
                await message.reply(note)
