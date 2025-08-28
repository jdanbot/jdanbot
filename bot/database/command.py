from tortoise import fields
from tortoise.fields import Field

from bot.database.lib.base_table import BaseTable


class Command(BaseTable):
    id: Field[int] | int = fields.IntField(
        default=None,
        primary_key=True,
    )

    chat_id: Field[int] | int = fields.IntField()
    user_id: Field[int] | int = fields.IntField()

    name: Field[str] | str = fields.TextField()
    args: Field[str] | str | None = fields.TextField(
        nullable=True,
        default=None,
    )
