from dataclasses import dataclass
from .message import MessageMock


@dataclass
class CallbackMock:
    message: MessageMock
