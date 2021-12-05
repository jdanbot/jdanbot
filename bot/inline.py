from .config import bot, dp, LANGS_LIST
from .lib.text import code, bold

from aiogram.types import InputTextMessageContent, \
                          InlineQueryResultAudio, InlineQueryResultArticle
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from wikipya.aiowiki import Wikipya
from bs4 import BeautifulSoup

from .lib import chez


@dp.chosen_inline_handler(lambda query: query.query.startswith("wiki"))
async def test(query):
    params = query.query.split(maxsplit=1)

    lang = params[0].split(":", maxsplit=1)
    lang = "ru" if len(lang) == 1 else lang[1]

    wiki = Wikipya(lang).get_instance()
    page_name = await wiki.get_page_name(query.result_id)
    page = await wiki.page(page_name)

    await bot.edit_message_text(
        inline_message_id=query.inline_message_id,
        text=page.parsed,
        parse_mode="HTML")


@dp.inline_handler(lambda query: True and
                   query.query.startswith("w") and
                   len(query.query.split(maxsplit=1)) == 2)
async def query_text(query):
    if not (query.query.endswith(".") or
            query.query.endswith("?") or
            query.query.endswith("!")):
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

        return await bot.answer_inline_query(query.id, btns)

    params = query.query.split(maxsplit=1)

    q = params[1]
    lang = params[0].split(":", maxsplit=1)
    lang = "ru" if len(lang) == 1 else lang[1]

    if not (lang in LANGS_LIST):
        return

    wiki = Wikipya(lang).get_instance()

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Загрузка...", callback_data="wait"))

    try:
        search = await wiki.search(q, 10)
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
                    parse_mode="HTML",
                )
            )
        ])

        return

    buttons = []

    for result in search:
        # page = await wiki.page(item)

        soup = BeautifulSoup(result.snippet, "lxml")

        buttons.append(InlineQueryResultArticle(
            id=result.page_id,
            title=result.title,
            description=soup.text[:100],
            input_message_content=InputTextMessageContent(
                message_text=soup.text,
                parse_mode="html"
            ),
            reply_markup=kb
        ))

    await bot.answer_inline_query(query.id, buttons)


@dp.inline_handler(lambda query: len(query.query) == 0)
async def inline_mode_menu(query):
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
