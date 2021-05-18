from .config import bot, dp, conn, notes, _, ADMIN_NOTES
from .lib import handlers
from .lib.admin import check_admin
from .lib.text import code, prettyword


@dp.message_handler(commands=["remove_note"])
@handlers.parse_arguments(2)
async def cool_secret(message, params):
    if params[1] in ADMIN_NOTES and message.chat.type == "supergroup":
        if await check_admin(message, bot):
            await notes.remove(message.chat.id, params[1])
        else:
            await message.reply(_("notes.no_rights_for_edit"))
    else:
        await notes.remove(message.chat.id, params[1])


@dp.message_handler(commands=["set"])
@handlers.parse_arguments(3)
async def set_(message, params):
    name = params[1][1:] if params[1].startswith("#") else params[1]

    if name in ADMIN_NOTES and message.chat.type == "supergroup":
        if await check_admin(message, bot):
            await notes.add(message.chat.id, name, params[2])
            await message.reply(_("notes.add_system_note"))
        else:
            await message.reply(_("notes.no_rights_for_edit"))
    else:
        await notes.add(message.chat.id, name, params[2])
        await message.reply(_("notes.add_note"))


@dp.message_handler(commands=["get"])
@handlers.parse_arguments(2)
async def get_(message, params):
    name = params[1][1:] if params[1].startswith("#") else params[1]

    if name == "__notes_list__":
        await message.reply(", ".join(await notes.show(message.chat.id)))
        return

    note = await notes.get(message.chat.id, name)

    if note is None:
        await message.reply(_("notes.create_var"))
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
            await message.reply(", ".join(await notes.show(chatid)))
        else:
            note = await notes.get(chatid, name)

            if note is None:
                return

            try:
                await message.reply(note, parse_mode="MarkdownV2")
            except Exception:
                await message.reply(note)
