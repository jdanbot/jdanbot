import asyncio
import ast
from aiogram.utils import json

from .aioget import aioget


class Anekru:
    def __init__(self):
        self.url = "https://www.anekdot.ru/rss/random.html"

    async def get_random(self) -> str:
        anek = await aioget(self.url)
        text = anek.text[135:-523]

        fixed_anek = ast.literal_eval(f"'{text}'")
        anek_parsed = "\n\n--------------\n\n".join(json.loads(fixed_anek))
        return anek_parsed.replace("<br>", "")


if __name__ == "__main__":
    anekru = Anekru()

    anek = asyncio.run(anekru.get_random())
    print(anek)
