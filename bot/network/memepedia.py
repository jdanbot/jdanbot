from aiogram import types

import pymemeru

from ..config import dp, _
from .. import handlers
from ..lib.models import Article

from tghtml import TgHTML


@dp.message_handler(commands=["memepedia", "meme"])
@handlers.send_article
@handlers.parse_arguments(1)
async def mempep(message: types.Message, query: str) -> Article:
    try:
        search = await pymemeru.search(query)
    except AttributeError:
        await message.reply(_("errors.not_found"))
        return

    page = await pymemeru.page(search[0].name)
    text = TgHTML(str(page.cleared_text)).parsed.replace('\n', '\n\n')

    text2 = f"""
<b>{page.title}</b>
<i>{page.published_at}</i> 👀 {page.views}\n
{text}
"""

    return Article(
        text=text2,
        image=page.main_image,
        test=True,
        href=f"https://memepedia.ru/{search[0].name}"
    )
