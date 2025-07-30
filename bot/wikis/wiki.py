from fluentogram import TranslatorRunner
import httpx
from aiogram import types, F
from aiogram.filters import Command, CommandObject
from aiogram.utils.markdown import code
from tghtml import TgHTML
from wikipya import Wikipya
from wikipya.constants import TAG_BLOCKLIST

from bot.filters.get_text import GetText

from .. import handlers
from ..config import WIKI_COMMANDS, WIKIPEDIA_SHORTCUTS, router
from ..config.languages import WIKIPEDIA_LANGS
from ..lib.models import Article
from ..lib.text import fix_words


@handlers.wikipya_handler("fallout")
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


@handlers.wikipya_handler("beholder")
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


async def check_mediawiki_api_url(url: str) -> bool:
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(url)

            return r.status_code == 200
    except Exception:
        return False


@handlers.wikipya_handler("lurk", "lurkmore")
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


@handlers.wikipya_handler("kaiser", "kaiserreich", "kr")
async def kaiser(message: types.Message) -> Wikipya:
    return Wikipya(
        base_url="https://kaiserreich.fandom.com/ru/api.php"
    )


@handlers.wikipya_handler("kaiseren", "kaiserreichen", "kre")
async def kaiser(message: types.Message) -> Wikipya:
    return Wikipya(base_url="https://kaiserreich.fandom.com/api.php")


@handlers.wikipya_handler("archwiki")
async def archwiki(message: types.Message) -> Wikipya:
    return Wikipya(
        base_url="https://wiki.archlinux.org/api.php", is_lurk=True
    )


@handlers.wikipya_handler("encycl")
async def encyclopedia(message: types.Message) -> Wikipya:
    return Wikipya(
        base_url="https://encyclopatia.ru/w/api.php",
        is_lurk=True,
        prefix="/wiki",
    )


@handlers.wikipya_handler("neolurk")
async def fallout(message: types.Message) -> Wikipya:
    return Wikipya(base_url="https://neolurk.org/w/api.php")


@handlers.wikipya_handler(
    "mediawiki", "mw", extract_query_from_url=True
)
async def custom_mediawiki(
    message: types.Message, command: CommandObject
) -> Wikipya:
    host = httpx.URL(command.args).host

    url_variants = [
        f"https://{host}/w/api.php",
        f"https://{host}/api.php",
    ]

    if not any(
        [
            await check_mediawiki_api_url(base_url := var)
            for var in url_variants
        ]
    ):
        await message.reply("Can't find valid API url")
        raise AttributeError

    return Wikipya(base_url=base_url)


@handlers.wikipya_handler(*WIKI_COMMANDS, went_trigger_command=True)
async def wikihandler(
    message: types.Message, trigger: str
) -> Wikipya:
    command = trigger.split()[0]
    lang = command.replace("/wiki", "").replace("/w", "")

    for lang_ in WIKIPEDIA_SHORTCUTS:
        if command[1:] in WIKIPEDIA_SHORTCUTS[lang_]:
            lang = lang_
            break

    if lang not in WIKIPEDIA_LANGS:
        lang = "ru"

    return Wikipya(
        lang, params=dict(tag_blocklist=["div.capsa-vicidata"])
    )


@router.message(
    Command("summary", "wiki"), GetText(disable_reply=True)
)
@handlers.send_article
async def get_summary(message: types.Message, query: str) -> Article:
    wiki = Wikipya("ru").get_instance()

    summary = await wiki.summary(query)

    try:
        image = summary.original_image.source
    except Exception:
        image = None

    return Article(
        text=fix_words(
            TgHTML(
                summary.extract_html, enable_preprocess=False
            ).parsed
        ),
        title=summary.title,
        href=summary.content_urls.desktop.page,
        image=image,
        parse_mode="html",
    )


@router.message(Command("s"))
@router.message(F.text.regexp("s(\w\w)").as_("lang"))
async def wikiSearch(
    message: types.Message, _: TranslatorRunner, lang: str = "ru"
):
    opts = message.text.split(maxsplit=1)

    if len(opts) == 1:
        await message.reply(
            _.enter_wiki_query().format(opts[0]),
            parse_mode="Markdown",
        )
        return

    return await message.reply(
        f"*Use bot's inline instead of this command\!*\nexample: {code(f"@jdan734_bot {lang} {(opts[1])}.")}"
    )
