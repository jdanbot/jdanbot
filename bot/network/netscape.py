import json
import sys
from datetime import datetime

from tghtml import TgHTML

import yaml

from ..config import dp, WIKIPYA_BLOCKLIST
from ..lib import handlers
from ..lib.aioget import aioget
from ..lib.convert_bytes import convert_bytes
from ..lib.text import code, cuteCrop
from ..lib.libtree import make_tree


@dp.message_handler(commands=["netscape"])
@handlers.only_jdan
@handlers.get_text
async def netscape(message, url):
    res = await aioget(url)

    print(res)
    html = await res.text()

    parsed_html = TgHTML(html, blocklist=WIKIPYA_BLOCKLIST)
    text = cuteCrop(str(parsed_html), limit=4096)

    await message.reply(text, parse_mode="HTML")
