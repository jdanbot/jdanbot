from aiogram import types
from wikipya import Wikipya

import httpx

from .. import handlers
from ..lib.text import fixWords
from ..config import dp, _, WIKI_COMMANDS, WIKIPEDIA_SHORTCUTS
from ..config.languages import WIKIPEDIA_LANGS

from ..lib.models import CustomField
from ..lib.models import Article

from tghtml import TgHTML

from aiogram.utils.markdown import escape_md


@handlers.wikipya_handler("lurk", "lurkmore")
async def lurkmore(message: types.Message) -> Wikipya:
    return Wikipya(
        base_url="https://lurkmore.rip/api.php",
        params=dict(
            tag_blocklist=[
                ["p", {"class": "quote_sign"}],
                ["div", {"class": "template"}],
                ["div", {"class": "thumb"}],
                ["img"],
                ["br"]
            ]
        )
    )


@handlers.wikipya_handler("fallout")
async def fallout(message: types.Message) -> Wikipya:
    return Wikipya(base_url="https://fallout.fandom.com/ru/api.php")


@handlers.wikipya_handler("kaiser", "kaiserreich")
async def kaiser(message: types.Message) -> Wikipya:
    return Wikipya(base_url="https://kaiserreich.fandom.com/ru/api.php")


@handlers.wikipya_handler("archwiki")
async def archwiki(message: types.Message) -> Wikipya:
    return Wikipya(base_url="https://wiki.archlinux.org/api.php", is_lurk=True)


@handlers.wikipya_handler("encycl")
async def encyclopedia(message: types.Message) -> Wikipya:
    return Wikipya(base_url="https://encyclopatia.ru/w/api.php", is_lurk=True, prefix="/wiki")


@handlers.wikipya_handler("mediawiki", extract_query_from_url=True)
async def custom_mediawiki(message: types.Message) -> Wikipya:
    url = message.get_full_command()[1].split("/")
    base_url = f"{'/'.join(url[:-2])}/api.php"

    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(base_url)

            assert r.status_code == 200
    except:
        base_url = f"{'/'.join(url[:3])}/w/api.php"

    return Wikipya(base_url=base_url)


@handlers.wikipya_handler(*WIKI_COMMANDS, went_trigger_command=True)
async def wikihandler(message: types.Message, trigger: str) -> Wikipya:
    command = trigger.split()[0]
    lang = command.replace("/wiki", "").replace("/w", "")

    for lang_ in WIKIPEDIA_SHORTCUTS:
        if command[1:] in WIKIPEDIA_SHORTCUTS[lang_]:
            lang = lang_
            break

    if lang not in WIKIPEDIA_LANGS:
        lang = "ru"

    return Wikipya(lang)


@dp.message_handler(commands=["summary", "wiki"])
@handlers.send_article
@handlers.parse_arguments_new
async def get_summary(
    message: types.message,
    query: CustomField(str)
) -> Article:
    wiki = Wikipya("ru").get_instance()

    summary = await wiki.summary(query)

    try:
        image = summary.original_image.source
    except Exception:
        image = None

    return Article(
        text=TgHTML(summary.extract_html, enable_preprocess=False).parsed,
        title=summary.title,
        href=summary.content_urls.desktop.page,
        image=image,
        parse_mode="html"
    )


@dp.message_handler(commands="s")
async def wikiSearch(message: types.Message, lang: str = "ru"):
    opts = message.text.split(maxsplit=1)

    if len(opts) == 1:
        await message.reply(_("errors.enter_wiki_query").format(opts[0]),
                            parse_mode="Markdown")
        return

    return await message.reply(
        f"*Use bot's inline instead of this command!*\nexample: `@jdan734_bot wiki {escape_md(opts[1])}.`",
        parse_mode="markdown"
    )

    query = opts[1]

    wiki = Wikipya(lang=lang).get_instance()

    r = await wiki.search(query, 10)

    if r == -1:
        await message.reply(_("error.not_found"))
        return

    kb = types.InlineKeyboardMarkup()
    for item in r:
        kb.add(
            types.InlineKeyboardButton(
                fixWords(item.title),
                callback_data=f"wikiru id{item.page_id}"
            )
        )

    await message.reply("Выберите результат поиска", reply_markup=kb, parse_mode="HTML")
