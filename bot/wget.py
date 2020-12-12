from .bot import dp
from .lib.html import code
from .lib.aioget import aioget

from datetime import datetime

import sys


@dp.message_handler(lambda message: message.from_user.id == 795449748,
                    commands=["d"])
async def download(message):
    options = message.text.split(maxsplit=1)

    if len(options) == 1:
        await message.reply("Напиши ссылку")
        return

    response = await aioget(options[1])
    text = await response.text()

    await message.reply(code(text[:4096]),
                        parse_mode="HTML")


@dp.message_handler(commands=["wget", "r", "request"])
async def wget(message):
    opt = message.text.split(maxsplit=1)
    if len(opt) == 1:
        await message.reply("Напиши ссылку")
        return

    time = datetime.now()
    url = opt[1]

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
        await message.reply(code(str(e)), parse_mode="HTML")
        return

    load_time = datetime.now() - time
    main = str(load_time).split(".")[0].split(":")

    page = await response.text()

    text = f"{url}\n"
    text += f"├─size:\n"
    text += f"│⠀├─bytes: {sys.getsizeof(page)}\n"
    text += f"│⠀└─megabytes: {str(sys.getsizeof(page) * (10**-6))}\n"
    text += f"└─time: {main[1]}:{main[2]}"

    await message.reply(code(text), parse_mode="HTML")
