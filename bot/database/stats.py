from pydantic import BaseModel
from ..config import settings
import httpx


class Statistics(BaseModel):
    users: int
    commands: int

    @classmethod
    async def get(cls) -> "Statistics":
        async with httpx.AsyncClient(base_url=settings.api_url) as client:
            return Statistics.parse_raw((await client.get("/stats")).text)


class ApiInfo(BaseModel):
    name: str
    version: str
    system: str

    @classmethod
    def get_sync(cls) -> "ApiInfo":
        return ApiInfo.parse_raw(httpx.get(f"{settings.api_url}/info").text)
