from aiogram import types
from httpx import AsyncClient
from bs4 import BeautifulSoup
from tghtml import TgHTML


from ..config import dp


@dp.message_handler(commands="slovnyk")
async def slovnyk(message: types.Message):
    command, text = message.get_full_command()
    print(text)

    async with AsyncClient() as client:
        r = await client.get("https://slovnyk.ua/index.php", params={"swrd": text})

    soup = BeautifulSoup(r.text, "lxml")

    _sum = soup.find_all(class_="toggle-sum")
    await message.reply(str(TgHTML(str(_sum[0]))), parse_mode="HTML")
