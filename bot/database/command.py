from typing import Optional
from odmantic import Model, Field

from pydantic_extra_types.pendulum_dt import DateTime
import pendulum as pdl


class Command(Model):
    user_id: int
    chat_id: int

    name: str
    args: Optional[str] = None

    runned_at: DateTime = Field(default_factory=pdl.now)
