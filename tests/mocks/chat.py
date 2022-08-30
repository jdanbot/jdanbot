from dataclasses import dataclass


@dataclass
class ChatMock:
    id: int = -10020000000
    type: str = "supergroup"

    title: str = "jdan's secret test chat"
    username: str = "savekanobu"

    async def restrict(self, *args, **kwargs) -> bool:
        # TODO: Implement restrict

        return True
