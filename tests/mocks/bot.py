from pydantic import BaseModel


class BotMock(BaseModel):
    token: str = None
    parse_mode: str = None
