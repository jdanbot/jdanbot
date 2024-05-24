from typing import Any, Iterable, Optional, TYPE_CHECKING
from tortoise import Tortoise, fields, run_async
from tortoise.fields import Field
from tortoise.models import Model

from aiogram import types

import pendulum as pdl

from datetime import datetime


class PdlField(Field[pdl.DateTime], pdl.DateTime):
    SQL_TYPE = "TIMESTAMP"

    class _db_mysql:
        SQL_TYPE = "DATETIME(6)"

    class _db_postgres:
        SQL_TYPE = "TIMESTAMPTZ"

    class _db_mssql:
        SQL_TYPE = "DATETIME2"

    class _db_oracle:
        SQL_TYPE = "TIMESTAMP WITH TIME ZONE"

    def __init__(
        self,
        auto_now: bool = False,
        auto_now_add: bool = False,
        **kwargs: Any,
    ) -> None:
        if auto_now_add and auto_now:
            raise AttributeError(
                "You can choose only 'auto_now' or 'auto_now_add'"
            )
        super().__init__(**kwargs)
        self.auto_now = auto_now
        self.auto_now_add = auto_now | auto_now_add

    def to_db_value(
        self, value: Optional[pdl.DateTime], instance
    ) -> Optional[str]:
        # Only do this if it is a Model instance, not class. Test for guaranteed instance var
        if hasattr(instance, "_saved_in_db") and (
            self.auto_now
            or (
                self.auto_now_add
                and getattr(instance, self.model_field_name) is None
            )
        ):
            value = pdl.now()
            setattr(instance, self.model_field_name, value)
            return str(value)

        if value is None:
            return value

        return pdl.instance(value).__str__()

    def to_python_value(
        self, value: str
    ) -> Optional[pdl.DateTime | pdl.Date | pdl.Time | pdl.Duration]:
        if value is None:
            return value

        if isinstance(value, datetime):
            return pdl.instance(value)

        return pdl.parse(value)


def unpack_needed(obj, fields: Iterable[str]) -> dict:
    def my_filter(el) -> bool:
        key, _ = el

        return key in fields

    try:
        obj = obj.model_dump()
    except AttributeError:
        pass

    items = obj.items()

    return dict(filter(my_filter, items))


class BaseModel(Model):
    @classmethod
    async def count(cls) -> int:
        return await cls.filter().count()

    async def update(self, data: dict):
        self.update_from_dict(data=data)

        return await self.save()

    class Meta:
        abstract = True


class User(BaseModel):
    id: Field[int] = fields.IntField(pk=True)

    first_name: Field[str] = fields.TextField()
    last_name: Optional[Field[str]] = fields.TextField(null=True)
    username: Optional[Field[str]] = fields.TextField(null=True)

    def __str__(self):
        return f"{self.id} {self.full_name}"

    @property
    def full_name(self) -> str:
        if self.last_name:
            return " ".join([self.first_name, self.last_name])

        return self.first_name

    @staticmethod
    async def get_by(message: types.Message) -> "User":
        return (
            await User.update_or_create(
                id=message.from_user.id,
                defaults=unpack_needed(
                    message.from_user,
                    {"username", "first_name", "last_name"},
                ),
            )
        )[0]


class Chat(BaseModel):
    id = fields.IntField(pk=True)

    title = fields.TextField()
    username = fields.TextField(null=True)

    def __str__(self):
        return self.title

    @staticmethod
    async def get_by(message: types.Message) -> "Chat":
        return (
            await Chat.update_or_create(
                id=message.chat.id,
                defaults=unpack_needed(
                    message.chat,
                    {"title", "username"},
                ),
            )
        )[0]


class Member_NoteExt:
    if TYPE_CHECKING:

        def __new__(cls, *args, **kwargs) -> "Member":
            return Member(chat=None)

    async def find_note(self, q: str) -> "Note":
        return await Note.find(self.chat.id, q)


class Member(Member_NoteExt, BaseModel):
    id = fields.IntField(pk=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User"
    )
    chat: fields.ForeignKeyRelation[Chat] = fields.ForeignKeyField(
        "models.Chat"
    )

    user_id: int
    chat_id: int

    def __str__(self):
        return f"Member {self.user_id}@{self.chat_id}"

    @staticmethod
    async def check_admin() -> bool:
        return True

    @staticmethod
    async def get_by(message: types.Message) -> "Member":
        return (
            await Member.get_or_create(
                chat=await Chat.get_by(message),
                user=await User.get_by(message),
            )
        )[0]


class Note(BaseModel):
    id: int = fields.IntField(pk=True)
    name: str = fields.TextField()
    text: str = fields.TextField()

    is_admin_note: bool = fields.BooleanField(null=True)

    author: fields.ForeignKeyRelation[Member] = (
        fields.ForeignKeyField("models.Member")
    )
    created_at: Field[pdl.DateTime] = PdlField(auto_now_add=True)

    editor: Optional[fields.ForeignKeyRelation[Member]] = (
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
        member: Member, name: str, text: str, is_admin_note: bool
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


async def init():
    await Tortoise.init(
        db_url="sqlite://tortoise.db",
        modules={"models": ["__main__"]},
    )

    await Tortoise.generate_schemas()

    print(pdl.now())

    user = types.User(
        id=1488,
        is_bot=False,
        first_name="TEST",
        last_name="Ankpfv",
        username="fegerg",
    )
    chat = types.Chat(
        id=-100500, type="t", title="test", username="mmm"
    )
    message = types.Message(
        message_id=4,
        date=datetime(2010, 3, 10),
        chat=chat,
        from_user=user,
    )

    m = await Member.get_by(message)

    # print(m)
    # print(await m.user)
    # print(await User.count())

    # print(await Note.find(200500, "test"))

    await Note.add(
        m,
        name="test",
        text="A long time ago in a galaxy far, far away....",
        is_admin_note=False,
    )

    note = await Note.find(-100500, "test")

    print(f"{note.edited_at=}")

    print(note.edited_at.time().diff(pdl.Time(20, 12, 20)))


run_async(init())
