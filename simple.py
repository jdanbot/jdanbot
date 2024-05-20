from typing import Optional
from tortoise import Tortoise, fields, run_async
from tortoise.models import Model

from datetime import datetime


class BaseModel(Model):
    @classmethod
    async def count(cls) -> int:
        return await cls.filter().count()

    @classmethod
    async def update(cls, data: dict):
        cls.update_from_dict(data)

        return await cls.save()

    class Meta:
        abstract = True


class User(BaseModel):
    id: int = fields.IntField(pk=True)

    first_name: str = fields.TextField()
    last_name: Optional[str] = fields.TextField(null=True)
    username: Optional[str] = fields.TextField(null=True)

    def __str__(self):
        return f"{self.id} {self.full_name}"

    @property
    def full_name(self) -> str:
        if self.last_name:
            return " ".join([self.first_name, self.last_name])

        return self.first_name

    @staticmethod
    async def get_by() -> "User":
        return await User.update_or_create(
            id=200,
            defaults=dict(
                first_name="BANHOPHer", username="ankopfov"
            ),
        )


class Chat(BaseModel):
    id = fields.IntField(pk=True)

    title: str = fields.TextField()
    username: Optional[str] = fields.TextField(null=True)

    def __str__(self):
        return self.title

    @staticmethod
    async def get_by() -> "Chat":
        return await Chat.update_or_create(
            id=200500,
            defaults=dict(title="tg group", username="unknown"),
        )


class Member(BaseModel):
    id = fields.IntField(pk=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User"
    )
    chat: fields.ForeignKeyRelation[Chat] = fields.ForeignKeyField(
        "models.Chat"
    )

    def __str__(self):
        return str(self.id)

    async def check_admin() -> bool:
        return True


class Note(BaseModel):
    id: int = fields.IntField(pk=True)
    name: str = fields.TextField()
    text: str = fields.TextField()

    is_admin_note: bool = fields.BooleanField(null=True)

    author: fields.ForeignKeyRelation[Member] = (
        fields.ForeignKeyField("models.Member")
    )
    created_at: datetime = fields.DatetimeField(auto_now_add=True)

    editor: Optional[fields.ForeignKeyRelation[Member]] = (
        fields.ForeignKeyField(
            "models.Member", null=True, related_name="models.Member"
        )
    )
    edited_at: Optional[datetime] = fields.DatetimeField(null=True)

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

        print(member)
        print(member.id)

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
                    edited_at=datetime.now(),
                    text=text,
                ),
            )

        return is_edit


async def init():
    # Here we connect to a SQLite DB file.
    # also specify the app name of "models"
    # which contain models from "app.models"
    await Tortoise.init(
        db_url="sqlite://tortoise.db",
        modules={"models": ["__main__"]},
    )
    # Generate the schema
    await Tortoise.generate_schemas()

    u = await User.get_by()
    c = await Chat.get_by()
    print(u)

    m = (
        await Member.get_or_create(
            defaults=dict(chat=c[0], user=u[0])
        )
    )[0]

    print(m)
    print(await m.user)
    print(await User.count())

    print(await Note.find(200500, "test"))
    print(
        await Note.add(
            m,
            name="test",
            text="A long time ago in a galaxy far, far away....",
            is_admin_note=False,
        )
    )
    note = await Note.find(200500, "test")

    print(note.edited_at)


run_async(init())
