from typing import Any, Callable, Optional, TYPE_CHECKING

from .lib import BaseModel, PdlField
from tortoise import fields
from tortoise.fields import Field

import pendulum as pdl

if TYPE_CHECKING:
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
    id: int = fields.IntField(pk=True)
    name: str = fields.TextField()
    text: str = fields.TextField()

    is_admin_note: bool = fields.BooleanField(null=True)

    author: fields.ForeignKeyRelation["Member"] = (
        fields.ForeignKeyField("models.Member")
    )
    created_at: Field[pdl.DateTime] = PdlField(auto_now_add=True)

    editor: Optional[fields.ForeignKeyRelation["Member"]] = (
        fields.ForeignKeyField(
            "models.Member", null=True, related_name="models.Member"
        )
    )
    edited_at: Field[pdl.DateTime] = PdlField(null=True)

    @staticmethod
    async def find(chat_id: int, query: str) -> Optional["Note"]:
        return await Note.filter(
            author__chat_id=chat_id, name=query
        ).first()

    @staticmethod
    async def add(
        member: "Member", name: str, text: str, is_admin_note: bool
    ) -> bool:
        if is_admin_note and not await member.check_admin():
            raise AttributeError

        res = await Note.find((await member.chat).id, name)
        is_edit = res is not None

        if not is_edit:
            await Note.create(
                name=name,
                text=text,
                author=member,
                is_admin_note=is_admin_note,
            )
        else:
            await res.update(
                data=dict(
                    editor=member,
                    edited_at=pdl.now(),
                    text=text,
                ),
            )

        return is_edit

    @staticmethod
    async def get(
        chat_id: int,
        name: str,
        default: Any = None,
        type: Callable[[str, Any], Any] = lambda x, y: x,
    ) -> Any:
        res = await Note.filter(
            author__chat_id=chat_id, name=name
        ).first()

        if res is None:
            return default

        return type(res.text, default)

    @staticmethod
    async def get_notes(chat_id: int) -> list["Note"]:
        return await Note.filter(author__chat_id=chat_id)

    @staticmethod
    async def get_notes_list(chat_id: int) -> list[str]:
        return await Note.filter(author__chat_id=chat_id).values_list(
            "name", flat=True
        )

    @staticmethod
    async def remove(member: "Member", name: str):
        note = await Note.filter(
            author__chat_id=member.chat_id, name=name
        ).first()

        if note is None:
            return note

        if note.is_admin_note and not await member.check_admin():
            raise AttributeError

        return await Note.filter(id=note.id).delete()


class Member_NoteExt:
    async def find_note(self: "Member", q: str) -> "Note":
        return await Note.find(self.chat.id, q)
