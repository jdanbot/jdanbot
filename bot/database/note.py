import datetime
from typing import Any, Callable, Optional

from pydantic import BaseModel

from . import tables as t
from .telegram import Member


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

    async def find(chat_id: int, query: str) -> Optional["Note"]:
        res = await (
            t.Note.select()
            .where(t.Note.author.chat.id == chat_id)
            .where(t.Note.name == query)
            .first()
        )

        if res is not None:
            return Note.parse_obj(res)

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

    def get(
        chat_id: int,
        name: str,
        default: Any = None,
        type: Callable[[str, Any], Any] = lambda x, y: x,
    ) -> Any:
        res = await (
            t.Note.select()
            .where(t.Note.member.chat.id == chat_id)
            .where(t.Note.name == name)
            .first()
        )

        if res is not None:
            return type(res)

    @staticmethod
    def show(
        chat_id: int, raw: bool = False
    ) -> list[str] | list["Note"]:
        notes = (
            Note.select()
            .join(ChatMember, on=Note.author == ChatMember.id)  # noqa
            .join(Chat, on=ChatMember.chat_id == Chat.id)  # noqa
            .where(Chat.id == chat_id)  # noqa
        )

        if raw:
            return notes
        else:
            return [note.name for note in notes]

    async def remove(member: Member, name: str):
        note = (
            Note.select()
            .join(ChatMember, on=Note.author_id == ChatMember.id)
            .join(Chat, on=ChatMember.chat_id == Chat.id)
            .where(Chat.id == member.chat.id, Note.name == name)
        )[0]

        if note.is_admin_note and not await member.check_admin():
            raise AttributeError

        return Note.delete().where(Note.id == note.id).execute()
