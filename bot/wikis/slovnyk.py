from aiogram import types
from bs4 import BeautifulSoup
from httpx import AsyncClient
from tghtml import TgHTML

from ..config import dp


@dp.message_handler(commands="slovnyk")
async def slovnyk(message: types.Message):
    _, text = message.get_full_command()

    async with AsyncClient() as client:
        r = await client.get("https://slovnyk.ua/index.php", params={"swrd": text})

    soup = BeautifulSoup(r.text, "lxml")

    _sum = soup.find_all(class_="toggle-sum")
    await message.reply(str(TgHTML(str(_sum[0]))), parse_mode="HTML")
