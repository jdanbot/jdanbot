from datetime import datetime
import io
from aiogram import types

from ..config import dp, _, settings
from ..schemas import Note, ChatMember, User
from .. import handlers

import humanize


@dp.message_handler(commands=["remove"])
@handlers.parse_arguments(1)
async def remove(message: types.Message, name: str):
    name = name[1:] if name.startswith("#") else name

    try:
        await Note.remove(ChatMember.get_by_message(message), name)
    except AttributeError:
        await message.reply(_("notes.no_rights_for_edit"))


@dp.message_handler(commands=["remove_bulk"])
@handlers.only_admins
@handlers.parse_arguments(1)
async def remove_bulk(message: types.Message, notes_raw: str):
    notes: list[str] = notes_raw.split()

    for note in notes:
        message.text = f"/remove {note}"
        await remove(message)


def build_user_info(user: User) -> str:
    return f"{user.full_name} (@{user.username}, {user.id})"


@dp.message_handler(commands=["export_notes"])
@handlers.only_admins
async def export_notes(message: types.Message):
    notes = Note.show(message.chat.id, raw=True)
    notes_raw = ""

    humanize.i18n.activate("ru_RU")

    for note in notes:
        notes_raw += f"{note.name} {'★' if note.is_admin_note else ''}\n"
        notes_raw += f"создал {build_user_info(note.author.user)} {humanize.naturaltime(note.created_at)}\n"

        if note.editor:
            notes_raw += f"изменил {build_user_info(note.editor.user)} {humanize.naturaltime(note.edited_at)}\n"

        notes_raw += f"\n{note.text}\n\n\n"

    f = io.StringIO(notes_raw)

    today = datetime.now().strftime("%d.%m.%Y")
    f.name = f"{message.chat.full_name.strip()} notes backup {today}.txt"

    await message.answer_document(f)


@dp.message_handler(commands=["set"])
@handlers.parse_arguments(2)
async def set_(message: types.Message, name: str, text: str):
    name = name[1:] if name.startswith("#") else name
    is_admin_note = name in settings.admin_notes

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

    note = Note.get(message.chat.id, name)

    if note is None:
        await message.reply(_("notes.create_var"))
        return

    try:
        await message.reply(note, parse_mode="MarkdownV2")
    except Exception:
        await message.reply(note)


@dp.message_handler(commands="show")
async def show(message: types.Message):
    await message.reply(", ".join(
        Note.show(message.chat.id)
    ))


@dp.message_handler(lambda message: message.text.startswith("#"))
async def use_by_hashtag(message: types.Message):
    message.text = message.text.removeprefix("#")

    name, *text = message.text.split(" ", maxsplit=1)
    text = text[0] if len(text) == 1 else ""

    if text != "" and (len(message.text) < 100 if message.is_forward() else True):
        message.text = f"/set {message.text}"
        return await set_(message)

    note = Note.get(message.chat.id, name)

    if note is None:
        return

    try:
        await message.reply(note, parse_mode="MarkdownV2")
    except Exception:
        await message.reply(note)
