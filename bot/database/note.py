from typing import TYPE_CHECKING, Any, Callable

from tortoise import fields
from tortoise.fields import Field

from .lib import BaseTable

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


class Note(BaseTable):
    id: int | Field[int] = fields.IntField(pk=True)
    chat_id: int | Field[int] = fields.IntField()

    name: str | Field[str] = fields.TextField()
    text: str | Field[str] = fields.TextField()

    is_admin_note: bool | Field[bool] = fields.BooleanField(null=True)

    author_id: int | Field[int] = fields.IntField()
    created_at: int | Field[int] = fields.IntField(null=True, default=None)

    editor_id: int | Field[int] = fields.IntField(null=True, default=None)

    #    author: fields.ForeignKeyRelation["Member"] = fields.ForeignKeyField("models.Member")
    #    created_at: Field[pdl.DateTime] = PendulumField(auto_now_add=True)

    #    editor: Optional[fields.ForeignKeyRelation["Member"]] = fields.ForeignKeyField(
    #        "models.Member", null=True, related_name="models.Member"
    #    )
    #    edited_at: Field[pdl.DateTime] = PendulumField(null=True)

    @staticmethod
    async def find(chat_id: int, query: str) -> "Note | None":
        return await Note.filter(chat_id=chat_id, name=query).first()

    @staticmethod
    async def add(member: "Member", name: str, text: str, is_admin_note: bool) -> bool:
        if is_admin_note and not await member.check_admin():
            raise AttributeError

        res: Note | None = await Note.find(
            chat_id=member.chat_id,
            query=name,
        )
        is_edit: bool = res is not None

        print(is_edit)
        print(res)

        if not is_edit:
            _ = await Note.create(
                name=name,
                text=text,
                chat_id=member.chat_id,
                author_id=member.user_id,
                is_admin_note=is_admin_note,
            )
        else:
            await res.update(
                data=dict(text=text, editor_id=member.user_id),
            )

        return is_edit

    @staticmethod
    async def get(
        chat_id: int,
        name: str,
        default: Any = None,
        type: Callable[[str, Any], Any] = lambda x, y: x,
    ) -> Any:
        res = await Note.filter(chat_id=chat_id, name=name).first()

        if res is None:
            return default

        return type(res.text, default)

    @staticmethod
    async def get_notes(chat_id: int) -> list["Note"]:
        return await Note.filter(chat_id=chat_id)

    @staticmethod
    async def get_notes_list(chat_id: int) -> list[str]:
        return await Note.filter(chat_id=chat_id).values_list("name", flat=True)

    @staticmethod
    async def remove(member: "Member", name: str):
        note = await Note.filter(chat_id=member.chat_id, name=name).first()

        if note is None:
            return note

        if note.is_admin_note and not await member.check_admin():
            raise AttributeError

        return await Note.filter(id=note.id).delete()


class Member_NoteExt:
    async def find_note(self: "Member", q: str) -> "Note":
        return await Note.find(self.chat.id, q)
