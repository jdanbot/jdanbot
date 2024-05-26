from typing import Optional

from tortoise import fields
import pendulum as pdl

from .lib import PdlField, BaseModel


class Command(BaseModel):
    id: int = fields.IntField(pk=True)

    chat_id: int = fields.BigIntField()
    user_id: int = fields.BigIntField()

    name: str = fields.TextField()
    args: Optional[str] = fields.TextField()

    runned_at: pdl.DateTime = PdlField(auto_now=True)
