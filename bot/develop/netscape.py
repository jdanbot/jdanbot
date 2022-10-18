from aiogram import types
from tghtml import TgHTML

from ..config import dp
from .. import handlers
from ..lib.aioget import aioget

from ..lib.models import Article, CustomField

from readability import Document


@dp.message_handler(commands=["netscape"], is_superuser=[946607335])
@handlers.send_article
@handlers.parse_arguments_new
async def netscape(message: types.Message, url: CustomField(str)) -> Article:
    res = await aioget(url)
    html = res.text

    parsed_html = TgHTML(html, enable_preprocess=True)
    title = Document(html).title()

    return Article(
        str(parsed_html),
        title=title,
        href=url,
        parse_mode="HTML",

        force_add_title=True
    )
