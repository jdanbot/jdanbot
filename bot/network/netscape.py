from tghtml import TgHTML

from ..config import dp
from ..lib import handlers
from ..lib.aioget import aioget
from ..lib.text import cuteCrop


@dp.message_handler(commands=["netscape"])
@handlers.only_jdan
@handlers.get_text
async def netscape(message, url):
    res = await aioget(url)
    html = res.text

    parsed_html = TgHTML(html)
    text = cuteCrop(str(parsed_html), limit=4096)

    await message.reply(text, parse_mode="HTML")
