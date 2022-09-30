from aiogram import types
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           InlineQueryResultArticle, InlineQueryResultAudio,
                           InputTextMessageContent)
from bs4 import BeautifulSoup
from wikipya.aiowiki import Wikipya

from .. import handlers
from ..config import WIKIPEDIA_LANGS, _, bot, dp
from ..lib import chez
from ..lib.kinorium import Kinorium
from ..lib.models import Article
from ..lib.text import bold, code, italic


@dp.chosen_inline_handler(lambda query: query.query.startswith("wiki"))
@handlers.send_article
async def test(query: types.CallbackQuery) -> Article:
    params = query.query.split(maxsplit=1)

    lang = params[0].split(":", maxsplit=1)
    lang = "ru" if len(lang) == 1 else lang[1]

    wiki = Wikipya(lang).get_instance()
    page_name = await wiki.get_page_name(query.result_id)
    page = await wiki.page(page_name)

    try:
        image = await wiki.image(page_name)
    except:
        image = type("FakeImage", (), {"source": None})

    opensearch = await wiki.opensearch(page_name)

    return Article(
        text=page.parsed,
        image=image.source,
        href=opensearch.results[0].link,
        params=dict(inline_message_id=query.inline_message_id),
    )


@dp.chosen_inline_handler(lambda query: query.query.startswith("kino"))
@handlers.send_article
async def test(query: types.CallbackQuery) -> Article:
    movie = await Kinorium.get(query.result_id)

    print(movie.rating)
    rating = movie.rating

    print(movie.parent_control)

    if len(movie.parent_control) > 0:
        parent = f"""
{bold("батьківський контроль")}:
{" | ".join([f'{prop.type_emoji}{prop.severity_emoji}' for prop in movie.parent_control])}"""
    else:
        parent = ""

    return Article(
        text=f"""
{bold(movie.name)} ({movie.published_at}) ⭐️ {rating.kinorium} 🧑‍💻 {str(rating.critics) + "%" if rating.critics != "—" else "—"}
{code(movie.original_name) + " " if movie.original_name else ""}[kinopoisk: {rating.kinopoisk}; imdb: {rating.imdb}]

{bold("довжина")}: {movie.duration}

{bold("країна")}: {', '.join(movie.countries)}
{bold("жанри")}: {', '.join(movie.genres)}{parent}

{movie.description or ''}""".strip(),
        image=movie.poster,
        href=f"https://ua.kinorium.com/{query.result_id}/",
        params=dict(inline_message_id=query.inline_message_id),
    )


@dp.inline_handler(lambda query: query.query == "")
async def inline_mode_menu(query):
    await bot.answer_inline_query(
        query.id,
        [
            InlineQueryResultArticle(
                id=4,
                title="Озвучить текст",
                description="Для использования введите @jdan734_bot <запрос>",
                input_message_content=InputTextMessageContent(
                    message_text="Мне нечего озвучивать. Введи текст"
                ),
            ),
            InlineQueryResultArticle(
                id=5,
                title="Найти в Википедии",
                description="Для использования введите @jdan734_bot wiki <запрос>",
                input_message_content=InputTextMessageContent(
                    message_text="Мне нечего находить. Введи запрос"
                ),
            ),
        ],
        cache_time=1,
    )


@dp.inline_handler(
    lambda query: query.query.startswith("kino")
    and len(query.query.split(maxsplit=1)) == 2
)
async def query_say(query):
    query.query = query.query.strip()

    if not (
        query.query.endswith(".")
        or query.query.endswith("?")
        or query.query.endswith("!")
    ):
        btns = [
            InlineQueryResultArticle(
                id=1,
                title="Поставь точку в конце!",
                description="Надо. Вставь.",
                input_message_content=InputTextMessageContent(
                    message_text="ПРОСТО ВСТАВЬ ТОЧКУ."
                ),
            )
        ]

        await bot.answer_inline_query(query.id, btns)

    query.query = query.query.removesuffix(".")

    cleared_query = query.query.split(" ", maxsplit=1)[1]

    movies = await Kinorium.search(cleared_query)

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Загрузка...", callback_data="wait"))

    await bot.answer_inline_query(
        query.id,
        [
            InlineQueryResultArticle(
                id=movie.id,
                title=movie.name,
                description=f'{f"{movie.original_name}; " if movie.original_name else ""}{movie.year}, жанри: {", ".join(movie.genres)}',
                thumb_url=movie.poster,
                thumb_width=60,
                thumb_height=95,
                input_message_content=InputTextMessageContent(
                    message_text=f'{f"{movie.original_name}; " if movie.original_name else ""}{movie.year}, жанри: {", ".join(movie.genres)}',
                    parse_mode="HTML",
                ),
                reply_markup=kb
            )
            for movie in movies
        ],
    )


@dp.inline_handler(
    lambda query: query.query.startswith("say")
    and len(query.query.split(maxsplit=1)) == 2
)
async def query_say(query):
    cleared_query = query.query.split(" ", maxsplit=1)[1]

    btns = [
        InlineQueryResultAudio(
            id=1, title=cleared_query, audio_url=chez.say(cleared_query)
        )
    ]

    await bot.answer_inline_query(query.id, btns)


@dp.inline_handler(
    lambda query: query.query.startswith("wiki")
    and len(query.query.split(maxsplit=1)) == 2
)
async def query_text(query: types.CallbackQuery):
    print("GLOBAL")

    params = query.query.split(maxsplit=1)

    if (lang := params[0]).removeprefix("wiki"):
        lang = lang if lang != "" else _("", return_lang=True)

    q = params[1]

    lang = "uk" if lang == "ua" else lang

    if lang not in WIKIPEDIA_LANGS:
        return

    wiki = Wikipya(lang).get_instance()

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Загрузка...", callback_data="wait"))

    try:
        search = await wiki.search_with_description(q, limit=10)
    except Exception as e:
        await bot.answer_inline_query(
            query.id,
            [
                InlineQueryResultArticle(
                    id=0,
                    title="При выполнении запроса возникла ошибка",
                    description=e,
                    input_message_content=InputTextMessageContent(
                        message_text=bold("При выполнении запроса возникла ошибка:")
                        + code(e),
                        parse_mode="HTML",
                    ),
                )
            ],
        )
        raise e

    buttons = []

    for result in search:
        try:
            image = result.thumbnail.source
        except Exception:
            image = None

        buttons.append(
            InlineQueryResultArticle(
                id=result.page_id,
                title=result.title,
                description=result.description,
                thumb_url=image,
                input_message_content=InputTextMessageContent(
                    message_text=result.description or result.title, parse_mode="html"
                ),
                reply_markup=kb,
            )
        )

    await bot.answer_inline_query(query.id, buttons)
