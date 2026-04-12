from aiogram import F, types
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InlineQueryResultAudio,
    InputTextMessageContent,
)
from aiogram.utils.markdown import bold, code
from wikipya.aiowiki import Wikipya

from ..config import WIKIPEDIA_LANGS, bot, router
from ..config.lib.spy_middleware import SpyMiddleware
from ..config.lib.tghtml import TgHTML
from ..lib import chez
from ..lib.models import Article
from ..wikis.wiktionary import get_word


@router.inline_query(F.query.len() == 0)
async def inline_mode_menu(inline_query: types.InlineQuery):
    await inline_query.answer(
        results=[
            InlineQueryResultArticle(
                id="4",
                title="Озвучить текст (не работает)",
                description="Для использования введите\n@jdan734_bot say <запрос>.",
                input_message_content=InputTextMessageContent(
                    message_text="Мне нечего озвучивать\\. Введи текст"
                ),
            ),
            InlineQueryResultArticle(
                id="5",
                title="Найти в Википедии (ru)",
                description="Для использования введите\n@jdan734_bot <запрос>.",
                input_message_content=InputTextMessageContent(
                    message_text="Мне нечего находить\\. Введи запрос"
                ),
            ),
            InlineQueryResultArticle(
                id="6",
                title="Найти в Википедии на языке lang",
                description="Для использования введите\n@jdan734_bot [lang] <запрос>.",
                input_message_content=InputTextMessageContent(
                    message_text="Мне нечего находить\\. Введи запрос"
                ),
            ),
            InlineQueryResultArticle(
                id="7",
                title="Найти в Викисловаре (ru)",
                description="Для использования введите\n@jdan734_bot v <запрос>.",
                input_message_content=InputTextMessageContent(
                    message_text="Мне нечего находить\\. Введи запрос"
                ),
            ),
            InlineQueryResultArticle(
                id="8",
                title="Найти в Викисловаре на языке lang",
                description="Для использования введите\n@jdan734_bot v[lang] <запрос>.",
                input_message_content=InputTextMessageContent(
                    message_text="Мне нечего находить\\. Введи запрос"
                ),
            ),
            InlineQueryResultArticle(
                id="9",
                title="Найти в Убежище (ru)",
                description="Для использования введите\n@jdan734_bot fallout <запрос>.",
                input_message_content=InputTextMessageContent(
                    message_text="Мне нечего находить\\. Введи запрос"
                ),
            ),
            InlineQueryResultArticle(
                id="10",
                title="Найти в ArchWiki (en)",
                description="Для использования введите\n@jdan734_bot arch <запрос>.",
                input_message_content=InputTextMessageContent(
                    message_text="Мне нечего находить\\. Введи запрос"
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
                message_text="ПРОСТО ВСТАВЬ ТОЧКУ.",
                parse_mode=None,
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


@router.inline_query(
    F.query.startswith("v")
    and ~(
        F.query.endswith(".")
        | F.query.endswith("?")
        | F.query.endswith("!")
    )
)
async def wiktionary(query: types.InlineQuery):
    q = query.query.strip()

    btns = [
        InlineQueryResultArticle(
            id="1",
            title="PING!!!!",
            description="Надо. Вставь.",
            input_message_content=InputTextMessageContent(
                message_text="ping",
                parse_mode=None,
            ),
        )
    ]

    await query.answer(btns)


FANDOMS = ["fallout", "beholder", "kaiserreich", "kr"]


def parse_lang_and_query(query: str) -> tuple[str, str]:
    params = query.removesuffix(".").split(maxsplit=1)

    if params[0] in WIKIPEDIA_LANGS:
        lang = params[0]
        params = params[1:]
    elif params[0] in FANDOMS:
        lang = params[0]
        params = params[1:]
    elif params[0] in ["archwiki", "arch"]:
        lang = params[0]
        params = params[1:]
    elif params[0] in ["v", "vde", "vru", "ven", "vte"]:
        lang = params[0]

        if lang == "v":
            lang = "vru"

        params = params[1:]
    else:
        lang = "ru"

    q = " ".join(params)
    return lang, q


@router.chosen_inline_result()
async def test(query: types.ChosenInlineResult) -> Article:
    lang, _ = parse_lang_and_query(query.query)

    if lang == "kr":
        lang = "kaiserreich"

    if lang in FANDOMS:
        wiki = Wikipya(
            base_url=f"https://{lang}.fandom.com/ru/api.php",
            params=dict(
                tag_blocklist=[
                    "div.cquote",
                ]
            ),
        )
    elif lang in ["arch", "archwiki"]:
        wiki = Wikipya(
            base_url="https://wiki.archlinux.org/api.php",
            params=dict(
                tag_blocklist=[
                    "div.archwiki-template-meta-related-articles"
                ]
            ),
        )
    elif lang in ["vru", "vde", "ven", "vte"]:
        lang = lang.removeprefix("v")

        if lang == "te":
            lang = "ru"
            inlang = "de"
        else:
            inlang = lang

        wiki = Wikipya(
            lang,
            base_url="https://{lang}.wiktionary.org/w/api.php",
        )

        page_name = await wiki.get_page_name(
            query.result_id
        )
        results = await get_word(lang, inlang, page_name)
        text = "\n\n".join(results)

        return await SpyMiddleware.send_article(
            query,
            Article(
                text=text[:4000],
                format_schema=(
                    "<blockquote expandable>{}</blockquote>"
                    if len(text) > 400
                    else "{}"
                ),
                title="page.title",
                disable_web_page_preview=True,
                href=f"https://{lang}/wiki/{page_name}",
            ),
        )
    else:
        wiki = Wikipya(lang)

    wiki.automatic_session_close=False

    page_name = await wiki.get_page_name(query.result_id)
    page = await wiki.page(page_name)

    try:
        image = (await wiki.image(page_name)).source
    except Exception:
        image = ""

    opensearch = await wiki.opensearch(page_name)
    await wiki.close()

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
            ".hatnote",
            "div#toc",
            "div.mbox-text-div",
            "span.hide-when-compact",
            "span.mbox-date",
            ".ts-disambig",
            *wiki.tag_blocklist,
        ],
    )

    text = x.output.strip()

    image: str | None = (
        None if image in (-1, "-1") else image
    )

    await SpyMiddleware.send_article(
        query,
        Article(
            text=text[:4000],
            format_schema=(
                "<blockquote expandable>{}</blockquote>"
                if len(text) > 400
                else "{}"
            ),
            image=image,
            title=page.title,
            disable_web_page_preview=not bool(image),
            href=opensearch.results[0].link,
        ),
    )


async def wiktionaryf(query: types.CallbackQuery):
    lang, q = parse_lang_and_query(query.query)

    lang = lang.removeprefix("v")

    if lang == "te":
        lang = "ru"
    
    wiki = Wikipya(
        lang,
        base_url="https://{lang}.wiktionary.org/w/api.php",
    )

    btn = InlineKeyboardButton(
        text="Загрузка...", callback_data="wait", style="primary"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[[btn]])

    try:
        search = await wiki.rest_search(q, limit=10)
    except Exception as e:
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

        raise e

    buttons = []

    for result in search:
        buttons.append(
            InlineQueryResultArticle(
                id=str(result.page_id),
                title=result.title,
                description=result.description,
                input_message_content=InputTextMessageContent(
                    message_text=result.description
                    or result.title,
                    parse_mode="html",
                ),
                reply_markup=kb,
            )
        )

    await bot.answer_inline_query(query.id, buttons)


@router.inline_query(F.query.len() > 0)
async def wikijewfrew(query: types.CallbackQuery):
    lang, q = parse_lang_and_query(query.query)

    if lang == "kr":
        lang = "kaiserreich"

    if lang in FANDOMS:
        wiki = Wikipya(
            base_url=f"https://{lang}.fandom.com/ru/api.php",
            params=dict(
                tag_blocklist=[
                    "div.cquote",
                ]
            ),
        )
    elif lang in ["arch", "archwiki"]:
        wiki = Wikipya(
            base_url="https://wiki.archlinux.org/api.php",
            params=dict(
                tag_blocklist=[
                    "div.archwiki-template-meta-related-articles"
                ]
            ),
        )
    elif lang in ["ven", "vde", "vru", "v", "vte"]:
        return await wiktionaryf(query)
    else:
        wiki = Wikipya(lang)

    btn = InlineKeyboardButton(
        text="Загрузка...", callback_data="wait",
        style="primary"

    )
    kb = InlineKeyboardMarkup(inline_keyboard=[[btn]])

    try:
        search = await wiki.search_with_description(
            q, limit=10
        )
    except Exception as e:
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

        raise e

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
                    message_text=result.description
                    or result.title,
                    parse_mode="html",
                ),
                reply_markup=kb,
            )
        )

    await bot.answer_inline_query(query.id, buttons)
