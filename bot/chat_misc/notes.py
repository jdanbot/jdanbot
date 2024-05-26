import contextlib
import io
from typing import Annotated, List

import humanize
import pendulum as pdl
from aiogram import F, types
from aiogram.filters import Command
from fluentogram import TranslatorRunner
from pydantic import BaseModel, RootModel, field_validator

from ..config import router, settings
from ..database import Member, Note, User, str2bool
from ..filters import Arguments, IsAdmin


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
    message: types.Message,
    args: NoteSelectModel,
    _: TranslatorRunner,
    member: Member,
):
    try:
        res = await Note.remove(member, args.key)

        if res is None:
            await message.reply("Заметка не найдена")

        else:
            await message.reply("Заметка успешно удалена")
    except AttributeError:
        await message.reply(_.no_rights_for_edit())


@router.message(Command("remove_bulk"), IsAdmin())
async def remove_bulk(message: types.Message):
    for note in message.text.split(" ")[1:]:
        message.text = f"/remove {note}"

        with contextlib.suppress(Exception):
            await remove(message)


def build_user_info(user: User) -> str:
    return f"{user.full_name} (@{user.username}, {user.id})"


@router.message(Command("export_notes"), IsAdmin())
async def export_notes(message: types.Message):
    humanize.i18n.activate("ru_RU")

    notes = await Note.get_notes(message.chat.id)
    notes_raw = ""

    for note in notes:
        await note.fetch_related("author")
        await note.author.fetch_related("user")

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

        note.editor = await note.editor

        if note.editor is not None:
            await note.editor.fetch_related("user")

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

    f = io.BytesIO(notes_raw.strip().encode())

    today = pdl.now().format("DD.MM.Y")
    name = f"{message.chat.full_name} notes backup {today}.txt"

    await message.answer_document(
        types.BufferedInputFile(f.read(), filename=name)
    )


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
            getattr(
                getattr(_, "edit" if is_edit else "add"),
                f"{'system_' if args.is_admin_note else ''}note",
            )(),
        )
    except AttributeError:
        await message.reply(_.no_rights_for_edit())


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
        ", ".join(await Note.get_notes_list(message.chat.id)),
        parse_mode=None,
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
