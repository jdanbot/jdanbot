from .bot import bot, dp

from wikipya.aiowiki import Wikipya

import traceback
import aiogram
import re


digits_pattern = re.compile(r'.{,}', re.MULTILINE)


@dp.inline_handler(lambda query: len(query.query) > 0)
async def query_text(query):
    try:
        matches = re.match(digits_pattern, query.query)

    except AttributeError as ex:
        return

    try:
        wiki = Wikipya("ru")
        q = matches.group()
        r = await wiki.search(q, 3)
        print(r)
        btns = []
        for page in r:
            p = await wiki.getPage(page[0])
            img = await wiki.getImageByPageName(page[0], 75)
            full_img = await wiki.getImageByPageName(page[0])
            if img != -1 and full_img != -1:
                t1 = re.sub("<b>", f'<a href="{full_img["source"]}">', wiki.parsePage(p), 1)
                t2 = re.sub("</b>", "</a>", t1, 1)
                btns.append(aiogram.types.InlineQueryResultArticle(
                        id=page[1], title=page[0],
                        description=p.text[:100],
                        input_message_content=aiogram.types.InputTextMessageContent(
                        message_text=t2,
                        parse_mode="HTML"),
                        thumb_url=img["source"], thumb_width=48, thumb_height=48
                ))
            else:
                btns.append(aiogram.types.InlineQueryResultArticle(
                        id=page[1], title=page[0],
                        description=p.text[:100],
                        input_message_content=aiogram.types.InputTextMessageContent(
                        message_text=wiki.parsePage(p),
                        parse_mode="HTML"),
                        thumb_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/75px-Wikipedia-logo-v2.svg.png", thumb_width=48, thumb_height=48
                ))
        await bot.answer_inline_query(query.id, btns)
    except Exception as e:
        print(traceback.format_exc())
