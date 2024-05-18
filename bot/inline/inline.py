from ..config import bot, WIKIPEDIA_LANGS, router
from aiogram.utils.markdown import code, bold

from aiogram import types, F
from aiogram.types import (
    InputTextMessageContent,
    InlineQueryResultAudio,
    InlineQueryResultArticle,
)
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from wikipya.aiowiki import Wikipya

from .. import handlers
from ..lib.models import Article

from ..lib import chez


@router.inline_query(F.query.startswith("w"))
async def query_text(query: types.CallbackQuery):
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

        return await bot.answer_inline_query(query.id, btns)

    params = query.query.split(maxsplit=1)

    q = params[1]
    lang = params[0].split(":", maxsplit=1)
    lang = "ru" if len(lang) == 1 else lang[1]

    if lang not in WIKIPEDIA_LANGS:
        return

    wiki = Wikipya(lang).get_instance()

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Загрузка...", callback_data="wait"))

    try:
        search = await wiki.search_with_description(q, limit=10)
    except Exception as e:
        print(e)
        await bot.answer_inline_query(
            query.id,
            [
                InlineQueryResultArticle(
                    id="0",
                    title="При выполнении запроса возникла ошибка",
                    description=e,
                    input_message_content=InputTextMessageContent(
                        message_text=bold(
                            "При выполнении запроса возникла ошибка:"
                        )
                        + code(e),
                        parse_mode="HTML",
                    ),
                )
            ],
        )

        return

    buttons = []

    for result in search:
        # soup = BeautifulSoup(result.snippet, "lxml")
        print(result)

        try:
            image = result.thumbnail.source
        except Exception:
            image = None

        buttons.append(
            InlineQueryResultArticle(
                id=str(result.page_id),
                title=result.title,
                description=result.description,
                thumb_url=image,
                input_message_content=InputTextMessageContent(
                    message_text=result.description or result.title,
                    parse_mode="html",
                ),
                reply_markup=kb,
            )
        )

    await bot.answer_inline_query(query.id, buttons)


@router.inline_query(F.query.len() == 0)
async def inline_mode_menu(inline_query: types.InlineQuery):
    await inline_query.answer(
        results=[
            InlineQueryResultArticle(
                id="4",
                title="Озвучить текст",
                description="Для использования введите @jdan734_bot say <запрос>",
                input_message_content=InputTextMessageContent(
                    message_text="Мне нечего озвучивать\. Введи текст"
                ),
            ),
            InlineQueryResultArticle(
                id="5",
                title="Найти в Википедии",
                description="Для использования введите @jdan734_bot wiki <запрос>",
                input_message_content=InputTextMessageContent(
                    message_text="Мне нечего находить\. Введи запрос"
                ),
            ),
        ],
        cache_time=1,
    )


@router.inline_query(F.query.startswith("say"))
@router.inline_query(F.query.len() > 0)
async def query_say(query: types.InlineQuery):
    q = query.query.strip()

    if q.endswith(".") or q.endswith("?") or q.endswith("!"):
        btns = [
            InlineQueryResultAudio(
                id="1",
                title=q[:-1],
                audio_url=chez.say(q),
            )
        ]

        await query.answer(btns)
    else:
        btns = [
            InlineQueryResultArticle(
                id="1",
                title="Поставь точку в конце!",
                description="Надо. Вставь.",
                input_message_content=InputTextMessageContent(
                    message_text="ПРОСТО ВСТАВЬ ТОЧКУ.",
                    parse_mode=None,
                ),
            )
        ]

        await query.answer(btns)


@router.inline_query(F.query.len() > 0)
@handlers.send_article
async def test(query: types.InlineQuery) -> Article:
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
