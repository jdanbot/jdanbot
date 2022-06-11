from aiogram import types

from tghtml import TgHTML
from wikipya import Wikipya

import httpx

from .. import handlers
from ..lib.text import bold, fixWords
from ..lib.models import Article
from ..config import dp, _, WIKICOMMANDS, UNIQUE_COMMANDS
from ..config.languages import WIKIPEDIA_LANGS


@handlers.wikipya_handler("railgun")
async def railgun(message: types.Message) -> Wikipya:
    return Wikipya(base_url="https://toarumajutsunoindex.fandom.com/api.php", is_lurk=True)


@handlers.wikipya_handler("fallout")
async def fallout(message: types.Message, test: str) -> Wikipya:
    return Wikipya(base_url="https://fallout.fandom.com/ru/api.php")


@handlers.wikipya_handler("kaiser", "kaiserreich")
async def kaiser(message: types.Message) -> Wikipya:
    return Wikipya(base_url="https://kaiserreich.fandom.com/ru/api.php", is_lurk=True)


@handlers.wikipya_handler("doom")
async def doom(message: types.Message) -> Wikipya:
    return Wikipya(base_url="https://doom.fandom.com/api.php", is_lurk=True)


@handlers.wikipya_handler("lurk")
async def Lurk(message: types.Message) -> Wikipya:
    return Wikipya(base_url="http://lurkmore.to/api.php", is_lurk=True, prefix="")


@handlers.wikipya_handler("lurk")
async def absurd(message: types.Message) -> Wikipya:
    return Wikipya(base_url="https://absurdopedia.net/w/api.php", is_lurk=True, prefix="/wiki")


@handlers.wikipya_handler("pizdec", "mrakopedia")
async def pizdec(message: types.Message) -> Wikipya:
    #TODO: Recheck foto getter
    return Wikipya(base_url="https://mrakopedia.net/w/api.php", is_lurk=False, prefix="/wiki")


@handlers.wikipya_handler("archwiki")
async def archwiki(message: types.Message) -> Wikipya:
    return Wikipya(base_url="https://wiki.archlinux.org/api.php", is_lurk=True)


@handlers.wikipya_handler("encycl")
async def encyclopedia(message: types.Message) -> Wikipya:
    return Wikipya(base_url="https://encyclopatia.ru/w/api.php", is_lurk=True, prefix="/wiki")


@handlers.wikipya_handler("mediawiki", extract_query_from_url=True)
async def custom_mediawiki(message: types.Message) -> Wikipya:
    try:
        message.text = message.reply_to_message.text
    except AttributeError:
        pass

    url = message.get_full_command()[1].split("/")
    base_url = f"{'/'.join(url[:3])}/api.php"

    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(base_url)

            assert r.status_code == 200
    except:
        base_url = f"{'/'.join(url[:3])}/w/api.php"

    return Wikipya(base_url=base_url)


@dp.message_handler(commands=["langs", "wikilangs", "wiki_langs"])
async def getLangs(message: types.Message):
    await message.reply(_("wiki.langs"), parse_mode="Markdown",
                        disable_web_page_preview=True)


@handlers.wikipya_handler(*WIKICOMMANDS, went_trigger_command=True)
async def wikihandler(message: types.Message, trigger: str) -> Wikipya:
    # TODO Save query info in buttons

    # try:
    #     message.text = message.reply_to_message.text
    # except AttributeError:
    #     pass

    command = trigger.split()[0]
    lang = command.replace("/wiki", "").replace("/w", "")

    for lang_ in UNIQUE_COMMANDS:
        if command[1:] in UNIQUE_COMMANDS[lang_]:
            lang = lang_
            break

    if lang not in WIKIPEDIA_LANGS:
        # return
        lang = "ru"

    return Wikipya(lang)


@handlers.wikipya_handler("w_dev", enable_experemental_navigation=True, went_trigger_command=True)
async def wikihandler(message: types.Message, trigger: str) -> Wikipya:
    try:
        message.text = message.reply_to_message.text
    except AttributeError:
        pass

    # message.text = trigger

    print(trigger)

    query = message.text.split(maxsplit=1)[1].split("#")

    print(query)

    if len(query) > 1:
        wiki = Wikipya(lang="ru").get_instance()

        search = await wiki.search(query[0])
        sections = (await wiki.sections(search[0].title)).sections

        section_id = [section for section in sections if section.title.lower() == query[1].lower()][0].index
    else:
        section_id = 0

    return Wikipya(lang="ru"), section_id


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


@dp.message_handler(commands="s_dev")
async def wikiSearch(message: types.Message, lang: str = "ru"):
    opts = message.text.split(maxsplit=1)

    if len(opts) == 1:
        await message.reply(_("errors.enter_wiki_query").format(opts[0]),
                            parse_mode="Markdown")
        return

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
                callback_data=f"wikiru id{item.page_id} 0"
            )
        )

    await message.reply("t", reply_markup=kb, parse_mode="HTML")


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
