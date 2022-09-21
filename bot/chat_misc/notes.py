import contextlib
import io
from datetime import datetime

import humanize
from aiogram import types

from .. import handlers
from ..config import _, dp, settings
from ..schemas import ChatMember, Note, User, str2bool
from ..lib.models import CustomField


@dp.message_handler(commands=["remove"])
@handlers.parse_arguments_new
async def remove(
    message: types.Message,
    key: CustomField(lambda x: x.removeprefix("#")),
):
    try:
        await Note.remove(ChatMember.get_by_message(message), key)
    except AttributeError:
        await message.reply(_("notes.no_rights_for_edit"))


@dp.message_handler(commands=["remove_bulk"], is_admin=True)
async def remove_bulk(message: types.Message):
    notes: list[str] = message.get_args().split()

    for note in notes:
        message.text = f"/remove {note}"

        with contextlib.suppress(Exception):
            await remove(message)


def build_user_info(user: User) -> str:
    return f"{user.full_name} (@{user.username}, {user.id})"


@dp.message_handler(commands=["export_notes"], is_admin=True)
async def export_notes(message: types.Message):
    notes = Note.show(message.chat.id, raw=True)
    notes_raw = ""

    humanize.i18n.activate("ru_RU")

    for note in notes:
        notes_raw += f"{note.name} {'★' if note.is_admin_note else ''}\n"

        try:
            build_user_info(note.author.user)
            is_normal = True
        except Exception:
            is_normal = False

        if is_normal:
            notes_raw += f"создал {build_user_info(note.author.user)} {humanize.naturaltime(note.created_at)}\n"

        if note.editor_id != 0 and note.editor:
            notes_raw += f"изменил {build_user_info(note.editor.user)} {humanize.naturaltime(note.edited_at)}\n"

        notes_raw += f"\n{note.text}\n\n\n"

    f = io.StringIO(notes_raw)

    today = datetime.now().strftime("%d.%m.%Y")
    f.name = f"{message.chat.full_name.strip()} notes backup {today}.txt"

    await message.answer_document(f)


@dp.message_handler(commands=["set"])
@handlers.parse_arguments_new
async def set_(
    message: types.Message,
    key: CustomField(lambda x: x.removeprefix("#")),
    value: CustomField(str, can_take_from_reply=True),
):
    is_admin_note = key in settings.admin_notes

    try:
        is_edit = await Note.add(
            ChatMember.get_by_message(message), key, value, is_admin_note
        )
        await message.reply(
            _(
                f"notes.{'edit' if is_edit else 'add'}_{'system_' if is_admin_note else ''}note"
            )
        )
    except AttributeError:
        await message.reply(_("notes.no_rights_for_edit"))


@dp.message_handler(commands=["get"])
@handlers.parse_arguments_new
async def get(
    message: types.Message,
    key: CustomField(lambda x: x.removeprefix("#")),
):
    note = Note.get(message.chat.id, key)

    if note is None:
        await message.reply(_("notes.create_var"))
        return

    try:
        await message.reply(note, parse_mode="MarkdownV2")
    except Exception:
        await message.reply(note)


@dp.message_handler(commands=["show", "notes"])
async def show(message: types.Message):
    await message.reply(", ".join(Note.show(message.chat.id)))


@dp.message_handler(lambda message: message.text.startswith("#"))
async def use_by_hashtag(message: types.Message):
    message.text = message.text.removeprefix("#")

    name, *text = message.text.split(" ", maxsplit=1)
    text = text[0] if len(text) == 1 else ""

    if Note.get(message.chat.id, "enable_inline_set_note", True, str2bool) and (text != "" and not message.is_forward()):
        message.text = f"/set {message.text}"
        return await set_(message)

    note = Note.get(message.chat.id, name)

    if note is None:
        return

    try:
        await message.reply(note, parse_mode="MarkdownV2")
    except Exception:
        await message.reply(note)
