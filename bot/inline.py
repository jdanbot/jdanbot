from .config import bot, dp
from .locale import locale

from aiogram.types import InputTextMessageContent, \
                          InlineQueryResultAudio, InlineQueryResultArticle
from wikipya.aiowiki import Wikipya, NotFound
from bs4 import BeautifulSoup
from random import randint, choice

from .lib import chez


@dp.inline_handler(lambda query: False or
                   query.query.startswith("wiki ") or
                   query.query.startswith("вики "))
async def query_text(query):
    q = query.query.split(maxsplit=1)[1]

    wiki = Wikipya("ru")
    search = await wiki.search(q, 3)

    buttons = []
    for item in search:
        page = await wiki.page(item)
        soup = BeautifulSoup(page.text, "lxml")
        text = page.fixed

        btn_defaults = {"id": page.pageid, "title": page.title,
                        "description": soup.text[:100],
                        "thumb_width": 48, "thumb_height": 48,
                        "input_message_content": InputTextMessageContent(
                            message_text=text,
                            parse_mode="HTML"
                        )}

        try:
            img = await page.image(75)
            buttons.append(InlineQueryResultArticle(**btn_defaults,
                                                    thumb_url=img.source))

        except NotFound:
            default_image = locale.default_wiki_image
            buttons.append(InlineQueryResultArticle(**btn_defaults,
                                                    thumb_url=default_image))

    await bot.answer_inline_query(query.id, buttons)


@dp.inline_handler(lambda query: len(query.query) == 0)
async def cock(query):
    cock_size = randint(0, 46)
    if cock_size == 46:
        cock_size = 1488

    person = choice(locale.persons)

    await bot.answer_inline_query(query.id, [
        InlineQueryResultArticle(
            id=5,
            title="Вычислить кок сайз",
            description="Новая иновационная система вычисляет длину члена"
                        " очень точно. Достаточно приложить хуй к экрану",
            input_message_content=InputTextMessageContent(
                message_text=f"🏳️‍🌈 Размер моего хуя *{cock_size}см*",
                parse_mode="Markdown"
            )
        ),

        InlineQueryResultArticle(
            id=6,
            title="Кто я из Профсоюза?",
            description="Определяет кто вы в профсоюзе. Точность 100%",
            input_message_content=InputTextMessageContent(
                message_text=f"В профсоюзе я *{person['name']}*\n\n"
                             f"__{person['description']}__",
                parse_mode="Markdown"
            )
        )
    ], cache_time=1)


@dp.inline_handler(lambda query: len(query.query) > 0)
async def query_say(query):
    query.query = query.query.strip()

    if query.query.endswith(".") or \
       query.query.endswith("?") or \
       query.query.endswith("!"):
        btns = [
            InlineQueryResultAudio(id=1, title="test",
                                   audio_url=chez.say(query.query))
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
