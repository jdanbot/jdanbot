from aiogram import types

from ..config import dp, _, settings
from ..schemas import Note, ChatMember
from .. import handlers


@dp.message_handler(commands=["remove"])
@handlers.parse_arguments(1)
async def remove(message: types.Message, name: str):
    name = name[1:] if name.startswith("#") else name

    try:
        await Note.remove(ChatMember.get_by_message(message), name)
    except AttributeError:
        await message.reply(_("notes.no_rights_for_edit"))


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

    if text != "":
        # TODO  --------------------
        # TODO  ADD CHECK ON FORWARD
        # TODO  --------------------

        message.text = "/set " + message.text
        return await set_(message)

    note = Note.get(message.chat.id, name)

    if note is None:
        return

    try:
        await message.reply(note, parse_mode="MarkdownV2")
    except Exception:
        await message.reply(note)
