from .bot import bot, dp
from .data import data

from wikipya.aiowiki import Wikipya

import traceback
import re

from aiogram.types import InputTextMessageContent, InlineQueryResultArticle


digits_pattern = re.compile(r'.{,}', re.MULTILINE)


@dp.inline_handler(lambda query: len(query.query) > 0)
async def query_text(query):
    try:
        matches = re.match(digits_pattern, query.query)
        q = matches.group()

    except AttributeError:
        return

    try:
        wiki = Wikipya("ru")
        r = await wiki.search(q, 7)

        btns = []
        for page in r:
            p = await wiki.getPage(page[0])
            img = await wiki.getImageByPageName(page[0], 75)
            full_img = await wiki.getImageByPageName(page[0])
            t = wiki.parsePage(p)

            btn_defaults = {"id": page[1], "title": page[0],
                            "description": p.text[:100],
                            "thumb_width": 48, "thumb_height": 48,
                            "input_message_content": InputTextMessageContent(
                                message_text=t,
                                parse_mode="HTML"
                            )}

            if img != -1 and full_img != -1:
                btns.append(InlineQueryResultArticle(
                                **btn_defaults,
                                thumb_url=img["source"]
                            ))
            else:
                btns.append(InlineQueryResultArticle(
                                **btn_defaults,
                                thumb_url=data["default_wiki_image"]
                            ))

        await bot.answer_inline_query(query.id, btns)
    except Exception:
        print(traceback.format_exc())
