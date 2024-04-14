from typing import Optional
from beanie import Document, Link

from pydantic_extra_types.pendulum_dt import DateTime
import pendulum as pdl

from .telegram import Member
from pydantic import Field


class Command(Document):
    member: Link[Member]
    command: str
    params: Optional[str] = str
    when_runned: DateTime = Field(default_factory=pdl.now)