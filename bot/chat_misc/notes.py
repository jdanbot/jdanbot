import contextlib
import io
from datetime import datetime
from typing import Annotated, List

import humanize
from aiogram import F, types
from aiogram.filters import Command
from pydantic import BaseModel, RootModel, field_validator


from ..config import router, settings
from ..database import Member, Note, User, str2bool
from ..filters import IsAdmin, Arguments
from fluentogram import TranslatorRunner


def remove_hash(x: str) -> str:
    return x.removeprefix("#")


class NoteSelectModel(BaseModel):
    key: str
    _normalize_key = field_validator("key")(remove_hash)


NotesSelectModel = RootModel[List[NoteSelectModel]]


class NoteUpdateModel(NoteSelectModel):
    value: Annotated[str, dict(reply=True)]

    @property
    def is_admin_note(self) -> bool:
        return self.key in settings.admin_notes


@router.message(Command("remove"), Arguments())
async def remove(
    message: types.Message, args: NoteSelectModel, _: TranslatorRunner
):
    try:
        await Note.remove(await Member.get_by(message), args.key)
    except AttributeError:
        await message.reply(_.no_rights_for_edit())


@router.message(Command("remove_bulk"), IsAdmin())
async def remove_bulk(message: types.Message):
    for note in message.text.split(" ")[1:]:
        print(note)
        message.text = f"/remove {note}"

        with contextlib.suppress(Exception):
            await remove(message)


def build_user_info(user: User) -> str:
    return f"{user.full_name} (@{user.username}, {user.id})"


@router.message(Command("export_notes"), IsAdmin())
async def export_notes(message: types.Message):
    notes = await Note.get_notes(message.chat.id)
    notes_raw = ""

    humanize.i18n.activate("ru_RU")

    for note in notes:
        notes_raw += (
            f"{note.name} {'★' if note.is_admin_note else ''}\n"
        )

        try:
            build_user_info(note.author.user)
            is_normal = True
        except Exception:
            is_normal = False

        if is_normal:
            notes_raw += (
                " ".join(
                    [
                        "создал",
                        build_user_info(note.author.user),
                        humanize.naturaltime(note.created_at),
                    ]
                )
                + "\n"
            )

        if note.editor is not None:
            note.editor = await Member.get_by_id(note.editor)

            notes_raw += (
                " ".join(
                    [
                        "изменил",
                        build_user_info(note.editor.user),
                        humanize.naturaltime(note.edited_at),
                    ]
                )
                + "\n"
            )

        notes_raw += f"\n{note.text}\n\n\n"

    f = io.StringIO(notes_raw)

    today = datetime.now().strftime("%d.%m.%Y")
    f.name = (
        f"{message.chat.full_name.strip()} notes backup {today}.txt"
    )

    await message.answer_document(f)


@router.message(Command("set"), Arguments())
async def set_(
    message: types.Message, args: NoteUpdateModel, _: TranslatorRunner
):
    try:
        is_edit = await Note.add(
            await Member.get_by(message),
            args.key,
            args.value.strip(),
            args.is_admin_note,
        )
        await message.reply(
            _.get(
                f"{'edit' if is_edit else 'add'}_"
                f"{'system_' if args.is_admin_note else ''}"
                "note"
            )
        )
    except AttributeError:
        await message.reply(_.get("no_rights_for_edit"))


@router.message(Command("get"), Arguments())
async def get(
    message: types.Message, args: NoteSelectModel, _: TranslatorRunner
):
    note = await Note.get(message.chat.id, args.key)

    if note is None:
        if message.from_user.id != -1:
            await message.reply(_.create_var())

        return

    try:
        await message.reply(note, parse_mode="MarkdownV2")
    except Exception:
        await message.reply(note)


@router.message(Command("show", "notes"))
async def show(message: types.Message):
    await message.reply(
        ", ".join(await Note.get_notes_list(message.chat.id))
    )


@router.message(F.message.text.startswith("#"))
async def use_by_hashtag(message: types.Message):
    message.text = message.text.removeprefix("#")

    name, *text = message.text.split(" ", maxsplit=1)
    text = text[0] if len(text) == 1 else ""

    if text == "":
        message.text = f"/get {name}"
        message.from_user.id = -1

        return await get(message)

    if await Note.get(
        message.chat.id, "enable_inline_set_note", False, str2bool
    ) and (text != "" and not message.is_forward()):
        message.text = f"/set {message.text}"
        return await set_(message)
