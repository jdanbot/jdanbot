import datetime
from typing import Any, Callable, Optional

from pydantic import BaseModel

from . import tables as t
from .member import Member


def str2bool(value: str, default: bool | None = None) -> bool | None:
    match value.strip().lower():
        case "true" | "yes" | "1":
            return True
        case "false" | "no" | "0":
            return False
        case _:
            return default


class Note(BaseModel):
    id: int
    name: str
    text: str

    is_admin_note: bool

    author: Member | int
    created_at: datetime.datetime

    editor: Optional[Member] | int = None
    edited_at: Optional[datetime.datetime] = None

    @staticmethod
    async def find(chat_id: int, query: str) -> Optional["Note"]:
        res = await (
            t.Note.select()
            .where(t.Note.author.chat.id == chat_id)
            .where(t.Note.name == query)
            .first()
        )

        if res is not None:
            return Note.model_validate(res)

    @staticmethod
    async def add(
        member: Member, name: str, text: str, is_admin_note: bool
    ) -> bool:
        if is_admin_note and not await member.check_admin():
            raise AttributeError

        res = await Note.find(member.chat.id, name)
        is_edit = res is not None

        if not is_edit:
            await t.Note.insert(
                t.Note(
                    name=name,
                    text=text,
                    author=member.id,
                    is_admin_note=is_admin_note,
                )
            )
        else:
            await t.Note.update(
                editor=member.id,
                edited_at=datetime.datetime.now(),
                text=text,
            ).where(t.Note.id == res.id)

        return is_edit

    @staticmethod
    async def get(
        chat_id: int,
        name: str,
        default: Any = None,
        type: Callable[[str, Any], Any] = lambda x, y: x,
    ) -> Any:
        res = await (
            t.Note.select()
            .where(t.Note.author.chat == chat_id)
            .where(t.Note.name == name)
            .first()
        )

        if res is None:
            return default

        return type(res["text"], default)

    @staticmethod
    async def get_notes(chat_id: int) -> list["Note"]:
        notes = await (
            t.Note.select(
                t.Note.all_columns(exclude=[t.Note.author]),
                t.Note.author.all_columns(),
                t.Note.author.user.all_columns(),
            )
            .where(t.Note.author.chat == chat_id)
            .output(nested=True)
        )

        return [Note.parse_obj(note) for note in notes]

    @staticmethod
    async def get_notes_list(chat_id: int) -> list[str]:
        return await (
            t.Note.select(t.Note.name)
            .where(t.Note.author.chat == chat_id)
            .output(as_list=True)
        )

    @staticmethod
    async def remove(member: Member, name: str):
        note = await (
            t.Note.select()
            .where(t.Note.author.chat == member.chat.id)
            .where(t.Note.name == name)
            .first()
        )

        if note.is_admin_note and not await member.check_admin():
            raise AttributeError

        return await t.Note.delete().where(Note.id == note.id)
