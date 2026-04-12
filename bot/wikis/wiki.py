import aiohttp
from aiogram import F, types
from aiogram.filters import Command, CommandObject
from aiogram.utils.markdown import code
from wikipya import Wikipya
from wikipya.constants import TAG_BLOCKLIST
from yarl import URL

from bot.filters.get_text import GetText

from ..config import router
from ..config.config import (
    WIKI_COMMANDS,
    WIKIPEDIA_SHORTCUTS,
)
from ..config.languages import WIKIPEDIA_LANGS
from ..config.lib.tghtml import TgHTML
from ..lib.models import Article
from ..lib.text import fix_words


@router.message(
    Command("fallout"), GetText(disable_reply=True)
)
async def fallout(message: types.Message) -> Wikipya:
    return Wikipya(
        base_url="https://fallout.fandom.com/ru/api.php",
        params=dict(
            tag_blocklist=[
                "div.cquote",
                *TAG_BLOCKLIST,
            ]
        ),
    )


@router.message(
    Command("blood"), GetText(disable_reply=True)
)
async def blood(message: types.Message) -> Wikipya:
    return Wikipya(
        base_url="https://www.blood-wiki.org/api.php",
        params=dict(
            tag_blocklist=[
                "div.cquote",
                "div.toccolours",
                *TAG_BLOCKLIST,
            ]
        ),
    )


@router.message(
    Command("beholder"), GetText(disable_reply=True)
)
async def beholder(message: types.Message) -> Wikipya:
    return Wikipya(
        base_url="https://beholder.fandom.com/ru/api.php",
        params=dict(
            tag_blocklist=[
                "div.cquote",
                *TAG_BLOCKLIST,
            ]
        ),
    )


@router.message(
    Command("lurk", "lurkmore"), GetText(disable_reply=True)
)
async def lurkmore(message: types.Message) -> Wikipya:
    return Wikipya(
        base_url="https://lurkmore.online/api.php",
        params=dict(
            tag_blocklist=[
                "p.quote_sign",
                "div.quote_wrapper",
                "div.template",
                "div.thumb",
                "img",
                "br",
                *TAG_BLOCKLIST,
            ]
        ),
    )


@router.message(
    Command("wtno"), GetText(disable_reply=True)
)
async def tno(message: types.Message) -> Wikipya:
    return Wikipya(
        base_url="https://the-new-order-last-days-of-europe.fandom.com/ru/api.php",
        params=dict(
            tag_blocklist=[
                "div.cquote",
                *TAG_BLOCKLIST,
            ]
        ),
    )


@router.message(
    Command("kaiser", "kaiserreich", "kr"),
    GetText(disable_reply=True),
)
async def kaiserru(message: types.Message) -> Wikipya:
    return Wikipya(
        base_url="https://kaiserreich.fandom.com/ru/api.php"
    )


@router.message(
    Command("kaiseren", "kaiserreichen", "kre"),
    GetText(disable_reply=True),
)
async def kaiser(message: types.Message) -> Wikipya:
    return Wikipya(
        base_url="https://kaiserreich.fandom.com/api.php"
    )


@router.message(
    Command("archwiki"), GetText(disable_reply=True)
)
async def archwiki(message: types.Message) -> Wikipya:
    return Wikipya(
        base_url="https://wiki.archlinux.org/api.php",
        params=dict(
            tag_blocklist=[
                "div.archwiki-template-meta-related-articles"
            ]
        ),
    )


@router.message(
    Command("encycl"), GetText(disable_reply=True)
)
async def encyclopedia(message: types.Message) -> Wikipya:
    return Wikipya(
        base_url="https://encyclopatia.ru/w/api.php"
    )


@router.message(
    Command("neolurk"), GetText(disable_reply=True)
)
async def neolurk(message: types.Message) -> Wikipya:
    return Wikipya(base_url="https://neolurk.org/w/api.php")


async def check_mediawiki_api_url(url: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            return r.status == 200


@router.message(
    Command("mediawiki", "mw"), GetText(disable_reply=True)
)
async def custom_mediawiki(
    message: types.Message, command: CommandObject
) -> dict[Wikipya, str]:
    host = URL(command.args).host

    url_variants = [
        f"https://{host}/api.php",
        f"https://{host}/w/api.php",
    ]

    if not any(
        
            await check_mediawiki_api_url(base_url := var)
            for var in url_variants
        
    ):
        return await message.reply(
            "Can't find valid API url"
        )

    url = URL(command.args)
    query = url.path.split("/")[-1].replace("_", " ")

    return Wikipya(base_url=base_url), query


@router.message(
    Command(*WIKI_COMMANDS), GetText(disable_reply=True)
)
async def wikihandler(
    message: types.Message, command: CommandObject
) -> tuple[Wikipya, str]:
    command, args = command.command, command.args
    lang = command.removeprefix("wiki").removeprefix("w")

    for lang_ in WIKIPEDIA_SHORTCUTS:
        if command in WIKIPEDIA_SHORTCUTS[lang_]:
            lang = lang_
            break

    if lang not in WIKIPEDIA_LANGS:
        lang = "ru"

    return Wikipya(
        lang,
        params=dict(
            tag_blocklist=[
                "div.capsa-vicidata",
                "div.side-box-flex",
                "span.navigation-not-searchable",
                ".ts-fix-template",
            ]
        ),
    ), args


@router.message(
    Command("summary", "wiki"), GetText(disable_reply=True)
)
async def get_summary(
    message: types.Message, query: str
) -> Article:
    wiki = Wikipya("ru")

    summary = await wiki.summary(query)

    try:
        image = summary.original_image.source
    except Exception:
        image = None

    return Article(
        text=fix_words(
            TgHTML(
                summary.extract_html,
                enable_preprocess=False,
            ).parsed
        ),
        title=summary.title,
        href=summary.content_urls.desktop.page,
        image=image,
        parse_mode="html",
    )


@router.message(Command("s"))
@router.message(
    F.text.startswith("/s"),
    F.text.func(
        lambda x: len(x.split(" ", maxsplit=1)[0]) == 4
    ),
    F.text.func(lambda x: not x.startswith("/scp")),
)
async def wikiSearch(message: types.Message):
    opts = message.text.split(maxsplit=1)
    lang = opts[0].removeprefix("/s") or "ru"
    query = opts[1] if len(opts) == 2 else "Название Статьи"

    return await message.reply(
        f"*Use bot's inline instead of this command*\nexample: {code(f'@jdan734_bot {lang} {query}.')}"
    )
