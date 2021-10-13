from .config import bot, dp, Note, _, ADMIN_NOTES
from .lib import handlers
from .lib.admin import check_admin


@dp.message_handler(commands=["remove", "remove_note"])
@handlers.parse_arguments(2)
async def cool_secret(message, params):
    params[1] = params[1][1:] if params[1].startswith("#") else params[1]

    if params[1] in ADMIN_NOTES and message.chat.type == "supergroup":
        if await check_admin(message, bot):
            Note.remove(message.chat.id, params[1])
        else:
            await message.reply(_("notes.no_rights_for_edit"))
    else:
        Note.remove(message.chat.id, params[1])


@dp.message_handler(commands=["set"])
@handlers.parse_arguments(3)
async def set_(message, params):
    # TODO: REWRITE: If note is created send edit text else created text

    name = params[1][1:] if params[1].startswith("#") else params[1]

    if name in ADMIN_NOTES and message.chat.type == "supergroup":
        if await check_admin(message, bot):
            Note.add(message.chat.id, name, params[2])
            await message.reply(_("notes.add_system_note"))
        else:
            await message.reply(_("notes.no_rights_for_edit"))
    else:
        Note.add(message.chat.id, name, params[2])
        await message.reply(_("notes.add_note"))


@dp.message_handler(commands=["get"])
@handlers.parse_arguments(2)
async def get_(message, params):
    name = params[1][1:] if params[1].startswith("#") else params[1]

    if name == "__notes_list__":
        await message.reply(", ".join(Note.show(message.chat.id)))
        return

    note = Note.get(message.chat.id, name)

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
    chat_id = message.chat.id

    if len(name) <= 50:
        if name == "__notes_list__":
            await message.reply(", ".join(Note.show(chat_id)))
        else:
            note = Note.get(chat_id, name)

            if note is None:
                return

            try:
                await message.reply(note, parse_mode="MarkdownV2")
            except Exception:
                await message.reply(note)
