from typing import Optional
from beanie import Document

from pydantic_extra_types.pendulum_dt import DateTime
import pendulum as pdl

from pydantic import Field


class Command(Document):
    user_id: int
    chat_id: int

    name: str
    params: Optional[str] = str

    runned_at: DateTime = Field(default_factory=pdl.now)
