from typing import Optional
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

from ..handlers.tghtml import TgHTML


@router.inline_query(F.query.len() == 0)
async def inline_mode_menu(inline_query: types.InlineQuery):
    await inline_query.answer(
        results=[
            InlineQueryResultArticle(
                id="4",
                title="Озвучить текст",
                description="Для использования введите @jdan734_bot say <запрос>.",
                input_message_content=InputTextMessageContent(
                    message_text="Мне нечего озвучивать\. Введи текст"
                ),
            ),
            InlineQueryResultArticle(
                id="5",
                title="Найти в Википедии",
                description="Для использования введите @jdan734_bot <запрос>.",
                input_message_content=InputTextMessageContent(
                    message_text="Мне нечего находить\. Введи запрос"
                ),
            ),
        ],
        cache_time=1,
    )


@router.inline_query(
    ~(
        F.query.endswith(".")
        | F.query.endswith("?")
        | F.query.endswith("!")
    )
)
async def dot_in_end_please(query: types.CallbackQuery):
    btns = [
        InlineQueryResultArticle(
            id="1",
            title="Поставь точку в конце!",
            description="Надо. Вставь.",
            input_message_content=InputTextMessageContent(
                message_text="ПРОСТО ВСТАВЬ ТОЧКУ.", parse_mode=None
            ),
        )
    ]

    return await bot.answer_inline_query(query.id, btns)


@router.inline_query(F.query.startswith("say"))
async def query_say(query: types.InlineQuery):
    q = query.query.strip()

    btns = [
        InlineQueryResultAudio(
            id="1",
            title=q[:-1],
            audio_url=chez.say(q),
        )
    ]

    await query.answer(btns)


def parse_lang_and_query(query: str) -> tuple[str, str]:
    params = query.split(maxsplit=1)

    if params[0] in WIKIPEDIA_LANGS:
        lang = params[0]
        params = params[1:]
    else:
        lang = "ru"

    q = " ".join(params)

    return lang, q


@router.chosen_inline_result()
@handlers.send_article
async def test(query: types.ChosenInlineResult) -> Article:
    lang, _ = parse_lang_and_query(query.query)

    wiki = Wikipya(lang).get_instance()
    page_name = await wiki.get_page_name(query.result_id)
    page = await wiki.page(page_name)

    try:
        image = (await wiki.image(page_name)).source
    except Exception:
        image = ""

    opensearch = await wiki.opensearch(page_name)

    x = TgHTML(
        page.text,
        blocklist=[
            "div.navigation-not-searchable",
            "table",
            ".error",
            ".noprint",
            ".thumb",
            "span.error",
            "span.mw-ext-cite-error",
            "p.hatnote",
        ],
    )

    text = x.output.strip()

    schema = (
        "<blockquote expandable>{}</blockquote>"
        if len(text) > 400
        else "{}"
    )

    image: Optional[str] = None if image in (-1, "-1") else image

    return Article(
        text=schema.format(text[:4000]),
        image=image,
        title=page.title,
        disable_web_page_preview=not bool(image),
        href=opensearch.results[0].link,
    )


@router.inline_query(F.query.len() > 0)
async def wikijewfrew(query: types.CallbackQuery):
    lang, q = parse_lang_and_query(query.query)

    wiki = Wikipya(lang).get_instance()

    btn = InlineKeyboardButton(
        text="Загрузка...", callback_data="wait"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[[btn]])

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
                    description=str(e),
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
