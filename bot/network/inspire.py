#           GNU AFFERO GENERAL PUBLIC LICENSE
#             Version 3, 19 November 2007

# Copyright (C) 2026 Daniel Zakharov <gzdan734@gmail.com>
# Copyright (C) 2022-2023 SandaruKasa <SandaruKasa@ya.ru>

# This file (inspirobot.py) was a part of SKTG repository
# and license should be clarified separately due of
# licenses difference

# Actual license can be obtained by the following link
# https://github.com/SandaruKasa/SKTG/raw/529f26637a75942ad29686ef348625097e355905/LICENSE


import datetime

import aiohttp
from aiogram.filters import Command

from ..config import bot, router


# TODO: allow user to choose xmas / inspirobot
@router.message(Command("inspire", "inspirobot"))
async def get_repology_package(message: types.Message):
    await bot.send_chat_action(
        message.chat.id, "upload_photo"
    )

    today = datetime.date.today()
    if (
        today.month == 12
        and today.day >= 20
        or today.month == 1
        and today.day <= 14
    ):
        site = "xmascardbot.com"
    else:
        site = "inspirobot.me"
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://{site}/api",
            params={"generate": "true"},
        ) as response:
            picture_url = await response.text()

    await message.reply_photo(
        photo=picture_url,
        caption="https://{site}/share?iuid={iuid}".format(
            site=site,
            iuid=picture_url.split(site)[-1].strip("/"),
        ),
        parse_mode=None,
    )
