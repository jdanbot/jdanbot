from aiogram import types
from aiogram.filters import Command
from bs4 import BeautifulSoup
from httpx import AsyncClient
from tghtml import TgHTML

from ..config import router
from ..filters import GetText
from ..lib.models.article import Article


@router.message(
    Command("slovnyk"), GetText(disable_reply=True)
)
async def slovnyk(
    message: types.Message, query: str
) -> Article:
    async with AsyncClient() as client:
        r = await client.get(
            "https://slovnyk.ua/index.php",
            params={"swrd": query},
        )

    soup = BeautifulSoup(r.text, "lxml")
    _sum = soup.find_all(class_="toggle-sum")

    return Article(
        text=TgHTML(str(_sum[0])).parsed, href=r.url
    )
