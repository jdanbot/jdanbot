from aiogram import types

from .config import bot, dp, Note, _, ADMIN_NOTES
from .lib import handlers
from .lib.admin import check_admin


@dp.message_handler(commands=["remove", "remove_note"])
@handlers.parse_arguments(1)
async def cool_secret(message: types.Message, name: str):
    name = name[1:] if name.startswith("#") else name

    if name in ADMIN_NOTES and message.chat.type == "supergroup":
        if await check_admin(message, bot):
            Note.remove(message.chat.id, name)
        else:
            await message.reply(_("notes.no_rights_for_edit"))
    else:
        Note.remove(message.chat.id, name)


@dp.message_handler(commands=["set"])
@handlers.parse_arguments(2)
async def set_(message: types.Message, name: str, text: str):
    # TODO: REWRITE: If note is created send edit text else created text

    name = name[1:] if name.startswith("#") else name

    if name in ADMIN_NOTES and message.chat.type == "supergroup":
        if await check_admin(message, bot):
            Note.add(message.chat.id, name, text)
            await message.reply(_("notes.add_system_note"))
        else:
            await message.reply(_("notes.no_rights_for_edit"))
    else:
        Note.add(message.chat.id, name, text)
        await message.reply(_("notes.add_note"))


@dp.message_handler(commands=["get"])
@handlers.parse_arguments(1)
async def get_(message: types.Message, name: str):
    name = name[1:] if name.startswith("#") else name

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
async def notes_(message: types.Message):
    name = message.text.replace("#", "")
    chat_id = message.chat.id

    if len(name) >= 50:
        return

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
