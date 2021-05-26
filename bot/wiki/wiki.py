from ..lib.text import bold, code, cuteCrop, fixWords
from ..config import (
    bot, dp, logging, WIKIPYA_BLOCKLIST, _,
    LANGS_LIST, UNIQUE_COMMANDS
)

from aiogram import types
from wikipya.aiowiki import Wikipya, NotFound


WGR_FLAG = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb" +
    "/8/85/Flag_of_Belarus.svg/1000px-Flag_of_Belarus.svg.png"
)

WRW_FLAG = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb" +
    "/5/50/Flag_of_Belarus_%281918%2C_1991%E2%80%931995%29.svg" +
    "/1000px-Flag_of_Belarus_%281918%2C_1991%E2%80%931995%29.svg.png"
)


async def wikiSearch(message, lang="ru", logs=False):
    opts = message.text.split(maxsplit=1)

    if len(opts) == 1:
        await message.reply(_("errors.enter_wiki_query").format(opts[0]),
                            parse_mode="Markdown")
        return

    query = opts[1]
    print(f"[Wikipedia Search {lang.upper()}] {query}")

    wiki = Wikipya(lang)

    r = await wiki.search(query, 20)

    if r == -1:
        await message.reply(_("error.not_found")) 
        return

    text = ""

    for item in r:
        text += bold(fixWords(item.title)) + "\n"
        text += f"└─/w_{item.pageid}\n"

    await message.reply(text, parse_mode="HTML")


async def getWiki(message=None, lang="ru", logs=False, name=None):
    wiki = Wikipya(lang)

    if name is None:
        opts = message.text.split(maxsplit=1)
        if len(opts) == 1:
            await message.reply(_("errors.enter_wiki_query").format(opts[0]),
                                parse_mode="Markdown")
            return

        name = opts[1]

    logging.info(f"[Wikipedia {lang.upper()}] {name}")
    # print(f"[Wikipedia {lang.upper()}] {name}")

    try:
        search = await wiki.search(name)

    except NotFound:
        await message.reply(_("errors.not_found"))
        return

    opensearch = await wiki.opensearch(search[0].title)
    url = opensearch[-1][0]

    page = await wiki.page(search[0])

    if page == -1:
        text = ""

    elif str(page) == "":
        text = ""

    else:
        page.blockList = WIKIPYA_BLOCKLIST
        text = fixWords(page.parsed)

    try:
        image = await page.image()
        image = image.source
    except AttributeError:
        pass
    except NotFound:
        image = -1

    keyboard = types.InlineKeyboardMarkup()

    try:
        name = search[0].title
    except KeyError:
        name = name

    try:
        url
    except NameError:
        url = f"https://{lang}.wikipedia.org/wiki/{name}"

    keyboard.add(types.InlineKeyboardButton(text=_("wiki.read_full"),
                                            url=url))

    if type(image) is int:
        await bot.send_chat_action(message.chat.id, "typing")
        try:
            await message.reply(cuteCrop(text, limit=4096), parse_mode="HTML",
                                reply_markup=keyboard)

        except Exception:
            pass

    else:
        if image == WGR_FLAG:
            image = WRW_FLAG

        await bot.send_chat_action(message.chat.id, "upload_photo")

        try:
            await message.reply_photo(image,
                                      caption=cuteCrop(text, limit=1024),
                                      parse_mode="HTML",
                                      reply_markup=keyboard)

        except Exception as e:
            await message.reply(bold(_("errors.error")) + "\n" + code(e),
                                parse_mode="HTML")


@dp.message_handler(commands=["langs", "wikilangs", "wiki_langs"])
async def getLangs(message):
    await message.reply(_("wiki.langs"), parse_mode="Markdown",
                        disable_web_page_preview=True)


wikicommands = []

for lang in LANGS_LIST:
    wikicommands.extend([f"wiki{lang}", f"w{lang}"])

for lang in UNIQUE_COMMANDS:
    wikicommands.extend(UNIQUE_COMMANDS[lang])


@dp.message_handler(commands=wikicommands)
async def wikihandler(message):
    command = message.text.split()[0]
    lang = command.replace("/wiki", "") \
                  .replace("/w", "")

    if lang in LANGS_LIST:
        await getWiki(message, lang)
        return

    else:
        for lang in UNIQUE_COMMANDS:
            if command[1:] in UNIQUE_COMMANDS[lang]:
                await getWiki(message, lang)
                break


@dp.message_handler(commands=["sru", "s", "search"])
async def wikis(message):
    await wikiSearch(message, "ru")


@dp.message_handler(commands=["wiki_usage"])
async def wiki_usage(message):
    await message.reply(_("wiki."), parse_mode="Markdown")


@dp.message_handler(lambda message: message.text.startswith("/w_"))
async def detect(message):
    text = message.text.replace("/w_", "")
    if text.find("@") != -1:
        text = text.split("@", maxsplit=1)[0]

    w = Wikipya("ru")

    try:
        id_ = int(text)

    except Exception:
        message.reply(_("errors.invalid_post_id"))
        return

    name = await w.getPageName(id_)

    if name == -1:
        await message.reply(_("errors.not_found"))
        return

    await getWiki(message, name=name)
