from aiogram import types

from tghtml import TgHTML
from wikipya import Wikipya

from ..lib import handlers
from ..lib.text import bold, fixWords
from ..lib.models import Article
from ..config import dp, _, WIKICOMMANDS, LANGS_LIST, UNIQUE_COMMANDS


@dp.message_handler(commands=["railgun"])
@handlers.wikipya_handler
async def railgun(message: types.Message) -> Wikipya:
    return Wikipya(base_url="https://toarumajutsunoindex.fandom.com/api.php", is_lurk=True)


@dp.message_handler(commands=["fallout"])
@handlers.wikipya_handler
async def fallout(message: types.Message) -> Wikipya:
    return Wikipya(base_url="https://fallout.fandom.com/ru/api.php", is_lurk=True, prefix="")


@dp.message_handler(commands=["kaiser", "kaiserreich"])
@handlers.wikipya_handler
async def kaiser(message: types.Message) -> Wikipya:
    return Wikipya(base_url="https://kaiserreich.fandom.com/ru/api.php", is_lurk=True)


@dp.message_handler(commands=["doom"])
@handlers.wikipya_handler
async def doom(message: types.Message) -> Wikipya:
    return Wikipya(base_url="https://doom.fandom.com/api.php", is_lurk=True)


@dp.message_handler(commands=["lurk"])
@handlers.wikipya_handler
async def Lurk(message: types.Message) -> Wikipya:
    return Wikipya(base_url="http://lurkmore.to/api.php", is_lurk=True, prefix="")


@dp.message_handler(commands=["absurd"])
@handlers.wikipya_handler
async def absurd(message: types.Message) -> Wikipya:
    return Wikipya(base_url="https://absurdopedia.net/w/api.php", is_lurk=True, prefix="/wiki")


@dp.message_handler(commands=["mrakopedia", "pizdec"])
@handlers.wikipya_handler
async def pizdec(message: types.Message) -> Wikipya:
    #TODO: Recheck foto getter
    return Wikipya(base_url="https://mrakopedia.net/w/api.php", is_lurk=True, prefix="/wiki")


@dp.message_handler(commands=["archwiki"])
@handlers.wikipya_handler
async def archwiki(message: types.Message) -> Wikipya:
    return Wikipya(base_url="https://wiki.archlinux.org/api.php", is_lurk=True)


@dp.message_handler(commands=["encycl"])
@handlers.wikipya_handler
async def encyclopedia(message: types.Message) -> Wikipya:
    return Wikipya(base_url="https://encyclopatia.ru/w/api.php", is_lurk=True, prefix="/wiki")


@dp.message_handler(commands=["langs", "wikilangs", "wiki_langs"])
async def getLangs(message: types.Message):
    await message.reply(_("wiki.langs"), parse_mode="Markdown",
                        disable_web_page_preview=True)


@dp.message_handler(commands=WIKICOMMANDS)
@handlers.wikipya_handler
async def wikihandler(message: types.Message) -> Wikipya:
    command = message.text.split()[0]
    lang = command.replace("/wiki", "").replace("/w", "")

    for lang_ in UNIQUE_COMMANDS:
        if command[1:] in UNIQUE_COMMANDS[lang_]:
            lang = lang_
            break

    if lang not in LANGS_LIST:
        return

    return Wikipya(lang)


@dp.message_handler(lambda message: message.text.startswith("/w_"))
@handlers.wikipya_handler
async def detect(message: types.Message) -> Wikipya:
    text = message.text.replace("/w_", "")

    if text.find("@") != -1:
        text = text.split("@", maxsplit=1)[0]

    try:
        id_ = int(text)

    except Exception:
        message.reply(_("errors.invalid_post_id"))
        return

    wiki = Wikipya("ru").get_instance()
    name = await wiki.get_page_name(id_)

    if name == -1:
        await message.reply(_("errors.not_found"))
    else:
        message.text = name

    return Wikipya("ru")


@dp.message_handler(commands="s")
async def wikiSearch(message: types.Message, lang: str = "ru"):
    opts = message.text.split(maxsplit=1)

    if len(opts) == 1:
        await message.reply(_("errors.enter_wiki_query").format(opts[0]),
                            parse_mode="Markdown")
        return

    query = opts[1]

    wiki = Wikipya(lang=lang).get_instance()

    r = await wiki.search(query, 20)

    if r == -1:
        await message.reply(_("error.not_found"))
        return

    text = ""

    for item in r:
        text += bold(fixWords(item.title)) + "\n"
        text += f"└─/w_{item.page_id}\n"

    await message.reply(text, parse_mode="HTML")


@dp.message_handler(commands="summary")
@handlers.send_article
@handlers.get_text
async def wiki_summary(message: types.Message, query: str) -> Article:
    wiki = Wikipya(lang="ru").get_instance()
    res = await wiki.summary(query)

    return Article(
        text=TgHTML(res.extract_html).parsed,
        image=res.original_image.source if res.original_image else None
    )
