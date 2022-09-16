from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class CustomField:
    type: Callable[[Any], Any]
    fallback: Callable[[Any], Any] | None = None
    can_take_from_reply: bool = False
    default: Any = "ReallyNone"
