from dataclasses import dataclass
from .message import MessageMock


@dataclass
class CallbackMock:
    message: MessageMock
    data: str

    async def answer(self, *args, **kwargs) -> bool:
        return True
