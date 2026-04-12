import contextlib
import io
from typing import Annotated

import humanize
from aiogram import F, types
from aiogram.filters import Command
from msgspec import Struct
from pydantic import BaseModel, RootModel, field_validator

from ..config import Locale, router, settings
from ..database import ChatSettings, Member, Note, User
from ..filters import Arguments, IsAdmin


def remove_hash(x: str) -> str:
    return x.removeprefix("#")


class NoteSelectModel(BaseModel):
    key: str
    _normalize_key = field_validator("key")(remove_hash)


NotesSelectModel = RootModel[list[NoteSelectModel]]


class NoteUpdateModel(NoteSelectModel):
    value: Annotated[str, dict(reply=True)]

    @property
    def is_admin_note(self) -> bool:
        return self.key in settings.admin_notes


class NoteUpdate(Struct, frozen=True):
    key: str
    value: str

    async def parse(
        message: types.Message,
        args: str,
        _: Locale,
        model: Struct,
    ) -> "NoteUpdate":
        key, value = args.split(maxsplit=2)

        return NoteUpdate(key=key, value=value)


@router.message(Command("remove"), Arguments())
async def remove(
    message: types.Message,
    args: NoteSelectModel,
    _: Locale,
):
    is_deleted = await Note.remove(
        message.chat.id, args.key
    )

    if is_deleted:
        await message.reply(_.notes.successful_deleted)
    else:
        await message.reply(_.notes.not_found)


@router.message(Command("remove_bulk"), IsAdmin())
async def remove_bulk(message: types.Message, _: Locale):
    for note in message.text.split(" ")[1:]:
        message = message.model_copy(
            update=dict(text=f"/remove {note}")
        )

        with contextlib.suppress(Exception):
            await remove(
                message,
                args=NoteSelectModel(key=note),
                _=_,
            )


def build_user_info(user: User) -> str:
    return f"{user.full_name} (@{user.username}, {user.id})"


@router.message(Command("export_notes"), IsAdmin())
async def export_notes(message: types.Message):
    import pendulum as pdl

    humanize.i18n.activate("ru_RU")

    notes = await Note.get_notes(message.chat.id)
    notes_raw = ""

    for note in notes:
        notes_raw += f"{note.name} {'★' if note.is_admin_note else ''}\n"

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
                        build_user_info(
                            await note.author.user.load()
                        ),
                        humanize.naturaltime(
                            note.created_at
                        ),
                    ]
                )
                + "\n"
            )

        if note.editor is not None:
            editor = await Member.get(id=note.editor.id)

            notes_raw += (
                " ".join(
                    [
                        "изменил",
                        build_user_info(
                            await editor.user.load()
                        ),
                        humanize.naturaltime(
                            note.edited_at
                            or pdl.datetime(0, 0, 0)
                        ),
                    ]
                )
                + "\n"
            )

        notes_raw += f"\n{note.text}\n\n\n"

    f = io.BytesIO(notes_raw.strip().encode())

    today = pdl.now().format("DD.MM.Y")
    name = (
        f"{message.chat.full_name} notes backup {today}.txt"
    )

    await message.answer_document(
        types.BufferedInputFile(f.read(), filename=name)
    )


@router.message(Command("set"), Arguments())
async def set_(
    message: types.Message,
    args: NoteUpdateModel,
    member: Member,
    _: Locale,
):
    is_note_added = await Note.add_or_update(
        member,
        args.key,
        args.value.strip(),
    )

    if is_note_added:
        await message.reply(_.notes.add_note)
    else:
        await message.reply(_.notes.edit_note)


@router.message(Command("get"), Arguments())
async def get(
    message: types.Message,
    args: NoteSelectModel,
    _: Locale,
):
    note = await Note.get(message.chat.id, args.key)

    if note is None:
        if message.from_user.id != -1:
            await message.reply(
                _.notes.create_var(name=args.key)
            )

        return

    try:
        await message.reply(
            note.text, parse_mode="MarkdownV2"
        )
    except Exception:
        await message.reply(note.text)


@router.message(Command("show", "notes"))
async def show(message: types.Message):
    await message.reply(
        ", ".join(
            await Note.get_notes_list(message.chat.id)
        )
        or "No notes",
        parse_mode=None,
    )


@router.message(Command("opt"), IsAdmin(), Arguments())
async def change(
    message: types.Message,
    args: NoteUpdate,
    member: Member,
):
    await member.chat.set_setting(args.key, args.value)
    await message.reply(
        "настройка установлена (наверно)", parse_mode=None
    )


@router.message(F.text.startswith("#"))
async def use_by_hashtag(
    message: types.Message,
    settings: ChatSettings,
    _: Locale,
):
    assert message.text

    text = message.text.removeprefix("#")

    name, *text = text.split(" ", maxsplit=1)
    text = text[0] if len(text) == 1 else None

    if text is None:
        message = message.model_copy(
            update=dict(
                text=f"/get {name}", from_user=dict(id=-1)
            )
        )

        return await get(
            message, args=NoteSelectModel(key=name), _=_
        )

    if settings.enable_inline_set_note and (
        message.forward_from is None
    ):
        x = message.text.split(" ", maxsplit=1)
        await set_(
            message.model_copy(
                update=dict(text=f"/set {message.text}")
            ),
            args=NoteUpdateModel(key=x[0], value=x[1]),
            _=_,
        )
