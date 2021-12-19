from aiogram import types
from tghtml import TgHTML

from ..config import dp
from ..lib import handlers
from ..lib.aioget import aioget
from ..lib.text import cute_crop


@dp.message_handler(commands=["netscape"])
@handlers.only_jdan
@handlers.get_text
async def netscape(message: types.Message, url: str):
    res = await aioget(url)
    html = res.text

    parsed_html = TgHTML(html)
    text = cute_crop(str(parsed_html), limit=4096)

    await message.reply(text, parse_mode="HTML")
