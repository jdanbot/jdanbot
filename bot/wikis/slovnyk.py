from aiogram import types
from bs4 import BeautifulSoup
from httpx import AsyncClient
from tghtml import TgHTML

from .. import handlers
from ..lib.models.article import Article

from ..config import dp


@dp.message_handler(commands="slovnyk")
@handlers.send_article
async def slovnyk(message: types.Message) -> Article:
    text = message.get_args()

    async with AsyncClient() as client:
        r = await client.get(
            "https://slovnyk.ua/index.php",
            params={"swrd": text}
        )

    soup = BeautifulSoup(r.text, "lxml")
    _sum = soup.find_all(class_="toggle-sum")

    return Article(
        text=TgHTML(str(_sum[0])).parsed,
        href=r.url
    )
