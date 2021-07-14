from .config import bot, dp, WIKIPYA_BLOCKLIST, _, LANGS_LIST
from .lib.text import code, bold

from aiogram.types import InputTextMessageContent, \
                          InlineQueryResultAudio, InlineQueryResultArticle
from wikipya.aiowiki import Wikipya, NotFound
from bs4 import BeautifulSoup
from random import randint, choice

from .lib import chez


@dp.inline_handler(lambda query: True and
                   query.query.startswith("w") and
                   len(query.query.split(maxsplit=1)) == 2)
async def query_text(query):
    params = query.query.split(maxsplit=1)

    q = params[1]
    lang = params[0].split(":", maxsplit=1)
    lang = "ru" if len(lang) == 1 else lang[1]

    if not (lang in LANGS_LIST):
        return

    wiki = Wikipya(lang)

    try:
        search = await wiki.search(q, 3)
    except Exception as e:
        print(e)
        await bot.answer_inline_query(query.id, [
            InlineQueryResultArticle(
                id=0,
                title="При выполнении запроса возникла ошибка",
                description=e,
                input_message_content=InputTextMessageContent(
                    message_text=bold("При выполнении запроса возникла ошибка:") +
                                 code(e),
                    parse_mode="HTML"
                )
            )
        ])

        return

    buttons = []

    for item in search:
        page = await wiki.page(item)
        page.blockList = WIKIPYA_BLOCKLIST

        soup = BeautifulSoup(page.text, "lxml")
        text = page.fixed

        btn_defaults = {"id": page.pageid, "title": page.title,
                        "description": soup.text[:100],
                        "input_message_content": InputTextMessageContent(
                            message_text=text,
                            parse_mode="HTML"
                        )}

        buttons.append(InlineQueryResultArticle(**btn_defaults))

    await bot.answer_inline_query(query.id, buttons)


@dp.inline_handler(lambda query: len(query.query) == 0)
async def cock(query):
    cock_size = randint(0, 46)

    if cock_size == 46:
        cock_size = 1488

    person = choice(_("triggers.persons")[0])

    await bot.answer_inline_query(query.id, [
        InlineQueryResultArticle(
            id=4,
            title="Озвучить текст",
            description="Для использования введите @jdan734_bot <запрос>",
            input_message_content=InputTextMessageContent(
                message_text="Мне нечего озвучивать. Введи текст"
            )
        ),

        InlineQueryResultArticle(
            id=5,
            title="Найти в Википедии",
            description="Для использования введите @jdan734_bot wiki <запрос>",
            input_message_content=InputTextMessageContent(
                message_text="Мне нечего находить. Введи запрос"
            )
        ),

        InlineQueryResultArticle(
            id=6,
            title="Вычислить cock size",
            description="Новая иновационная система вычисляет длину члена"
                        " очень точно. Достаточно приложить хуй к экрану",
            input_message_content=InputTextMessageContent(
                message_text=f"🏳️‍🌈 Размер моего хуя *{cock_size}см*",
                parse_mode="Markdown"
            )
        ),

        InlineQueryResultArticle(
            id=7,
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
            InlineQueryResultAudio(
                id=1, 
                title=query.query[:-1],
                audio_url=chez.say(query.query)
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
