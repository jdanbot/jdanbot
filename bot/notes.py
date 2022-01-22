from aiogram import types

from .config import dp, _, ADMIN_NOTES
from .database import Note, ChatMember
from .lib import handlers


@dp.message_handler(commands=["remove", "remove_note"])
@handlers.parse_arguments(1)
async def cool_secret(message: types.Message, name: str):
    name = name[1:] if name.startswith("#") else name

    try:
        await Note.remove(ChatMember.get_by_message(message), name)
    except AttributeError:
        await message.reply(_("notes.no_rights_for_edit"))


@dp.message_handler(commands=["set"])
@handlers.parse_arguments(2)
async def set_(message: types.Message, name: str, text: str):
    name = name[1:] if name.startswith("#") else name
    is_admin_note = name in ADMIN_NOTES

    try:
        is_edit = await Note.add(ChatMember.get_by_message(message), name, text, is_admin_note)
        await message.reply(_(
            f"notes.{'edit' if is_edit else 'add'}_{'system_' if is_admin_note else ''}note"))
    except AttributeError:
        await message.reply(_("notes.no_rights_for_edit"))


@dp.message_handler(commands=["get"])
@handlers.parse_arguments(1)
async def get(message: types.Message, name: str):
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
async def get_by_hashtag(message: types.Message):
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
