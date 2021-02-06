from .bot import bot, dp
from .data import data

from wikipya.aiowiki import Wikipya


from .lib import chez
import traceback
import re

from aiogram.types import InlineQueryResultDocument, InputTextMessageContent, \
                          InlineQueryResultAudio, InlineQueryResultArticle


digits_pattern = re.compile(r'.{,}', re.MULTILINE)


@dp.inline_handler(lambda query: query.query.startswith("wiki ") or
                                 query.query.startswith("вики "))  # noqa: E127
async def query_text(query):
    print(query.query)
    try:
        matches = re.match(digits_pattern, query.query)
        q = matches.group()

    except AttributeError:
        return

    try:
        wiki = Wikipya("ru")
        search = await wiki.search(q, 15)

        buttons = []
        for page in search:
            html = await wiki.getPage(page[0])
            img = await wiki.getImageByPageName(page[0], 75)
            full_img = await wiki.getImageByPageName(page[0])
            text = wiki.parsePage(html)

            btn_defaults = {"id": page[1], "title": page[0],
                            "description": html.text[:100],
                            "thumb_width": 48, "thumb_height": 48,
                            "input_message_content": InputTextMessageContent(
                                message_text=text,
                                parse_mode="HTML"
                            )}

            if img != -1 and full_img != -1:
                buttons.append(InlineQueryResultArticle(
                                   **btn_defaults,
                                   thumb_url=img["source"]
                               ))
            else:
                buttons.append(InlineQueryResultArticle(
                                   **btn_defaults,
                                   thumb_url=data["default_wiki_image"]
                               ))

        await bot.answer_inline_query(query.id, buttons)
    except Exception:
        print(traceback.format_exc())


@dp.inline_handler(lambda query: len(query.query) > 0)
async def query_say(query):
    print(f"{query.query = }")
    query.query = query.query.strip()

    if query.query.endswith(".") or \
       query.query.endswith("?") or \
       query.query.endswith("!"):
        btns = [
            InlineQueryResultAudio(
                id=1, title="test", audio_url=chez.say(query.query)
            )
        ]

        await bot.answer_inline_query(query.id, btns)
    else:
        btns = [
            InlineQueryResultArticle(
                id=1,
                title="Поставь точку в конце!",
                description="Надо. Вставь.",
                input_message_content=InputTextMessageContent(
                    message_text="ПРОСТО ВСТАВЬ ТОЧКУ."
                )
            )
        ]

        await bot.answer_inline_query(query.id, btns)
