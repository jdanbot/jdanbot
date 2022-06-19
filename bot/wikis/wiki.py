from aiogram import types
from wikipya import Wikipya

import httpx

from .. import handlers
from ..lib.text import fixWords
from ..config import dp, _, WIKI_COMMANDS, WIKIPEDIA_SHORTCUTS
from ..config.languages import WIKIPEDIA_LANGS


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
    return Wikipya(base_url="https://fallout.fandom.com/ru/api.php", is_lurk=True)


@handlers.wikipya_handler("kaiser", "kaiserreich")
async def kaiser(message: types.Message) -> Wikipya:
    return Wikipya(base_url="https://kaiserreich.fandom.com/ru/api.php", is_lurk=True)


@handlers.wikipya_handler("archwiki")
async def archwiki(message: types.Message) -> Wikipya:
    return Wikipya(base_url="https://wiki.archlinux.org/api.php", is_lurk=True)


@handlers.wikipya_handler("encycl")
async def encyclopedia(message: types.Message) -> Wikipya:
    return Wikipya(base_url="https://encyclopatia.ru/w/api.php", is_lurk=True, prefix="/wiki")


@handlers.wikipya_handler("mediawiki", extract_query_from_url=True)
async def custom_mediawiki(message: types.Message) -> Wikipya:
    url = message.get_full_command()[1].split("/")
    base_url = f"{'/'.join(url[:3])}/api.php"

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


@dp.message_handler(commands="s")
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
                callback_data=f"wikiru id{item.page_id}"
            )
        )

    await message.reply("Выберите результат поиска", reply_markup=kb, parse_mode="HTML")
