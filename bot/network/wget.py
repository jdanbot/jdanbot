import json
import sys
from datetime import datetime

import yaml

from ..config import dp
from ..lib import handlers
from ..lib.aioget import aioget
from ..lib.convert_bytes import convert_bytes
from ..lib.text import code
from ..lib.libtree import make_tree


@dp.message_handler(commands=["d"])
@handlers.only_jdan
@handlers.get_text
async def download(message, query):
    response = await aioget(query)
    text = await response.text()

    try:
        text = yaml.dump(json.loads(text))
    except json.decoder.JSONDecodeError:
        pass

    await message.reply(code(text[:4096]),
                        parse_mode="HTML")


@dp.message_handler(commands=["wget", "r", "request"])
@handlers.parse_arguments(2)
async def wget(message, params):
    time = datetime.now()
    url = params[1]

    blacklist = ["mb", ".zip", ".7", ".gz", "98.145.185.175", ".avi",
                 "movie", "release", ".dll", "localhost", ".bin",
                 "0.0.0.1", "repack", "download"]

    if url.find("?") != -1:
        if url.split("/")[-1][:url.find("?")].find(".") != -1:
            await message.reply("Бан")
            return

    for word in blacklist:
        if url.lower().find(word) != -1:
            await message.reply("Ваша ссылка в черном списке")
            return

    try:
        response = await aioget(url)
    except Exception as e:
        await message.reply(code(e), parse_mode="HTML")
        return

    load_time = datetime.now() - time
    main = str(load_time).split(":")

    page = await response.text()

    tree = make_tree({
        "status": response.status,
        "size": convert_bytes(sys.getsizeof(page)),
        "time": f"{main[1]}:{main[2][:main[2].find('.')]}"
    }, url)

    await message.reply(code(tree), parse_mode="HTML")
