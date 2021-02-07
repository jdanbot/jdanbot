from .lib.fixWords import fixWords
from .lib.cutecrop import cuteCrop
from .lib.html import bold
from .data import data
from .config import bot, dp, logger


import aiogram

from wikipya.aiowiki import Wikipya, NotFound


async def wikiSearch(message, lang="ru", logs=False):
    opts = message.text.split(maxsplit=1)
    if len(opts) == 1:
        await message.reply(data["wikierror"].format(opts[0]),
                            parse_mode="Markdown")
        return

    query = opts[1]
    print(f"[Wikipedia Search {lang.upper()}] {query}")

    wiki = Wikipya(lang)

    r = await wiki.search(query, 20)

    if r == -1:
        await message.reply("Ничего не найдено")
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
            await message.reply(data["wikierror"].format(opts[0]),
                                parse_mode="Markdown")
            return

        name = opts[1]

    logger.debug(f"[Wikipedia {lang.upper()}] {name}")
    # print(f"[Wikipedia {lang.upper()}] {name}")

    try:
        search = await wiki.search(name)

    except NotFound:
        await message.reply("Ничего не найдено")
        return

    opensearch = await wiki.opensearch(search[0].title)
    url = opensearch[-1][0]

    page = await wiki.page(search[0])

    if page == -1:
        text = ""

    elif str(page) == "":
        text = ""

    else:
        page.blockList = [["table", {"class": "infobox"}],
                          ["ol", {"class": "references"}],
                          ["link"], ["style"],
                          ["table", {"class": "noprint"}]]
        text = fixWords(page.parsed)

    try:
        image = await page.image()
        image = image.source
    except AttributeError:
        pass
    except NotFound:
        image = -1

    keyboard = aiogram.types.InlineKeyboardMarkup()

    try:
        name = search[0].title
    except KeyError:
        name = name

    try:
        url
    except NameError:
        url = f"https://{lang}.wikipedia.org/wiki/{name}"

    keyboard.add(aiogram.types.InlineKeyboardButton(text="Читать полностью",
                                                    url=url))

    if type(image) is int:
        await bot.send_chat_action(message.chat.id, "typing")
        try:
            await message.reply(cuteCrop(text, limit=4096), parse_mode="HTML",
                                reply_markup=keyboard)

        except Exception:
            pass

    else:
        if image == data["belarus_flag"]["old"]:
            image = data["belarus_flag"]["new"]

        await bot.send_chat_action(message.chat.id, "upload_photo")

        try:
            await message.reply_photo(image, caption=cuteCrop(text, limit=1024),
                                      parse_mode="HTML",
                                      reply_markup=keyboard)

        except Exception as e:
            await message.reply(f"*Не удалось отправить статью*\n`{e}`",
                                parse_mode="Markdown")


@dp.message_handler(commands=["langs", "wikilangs", "wiki_langs"])
async def langs(message):
    await message.reply(data["langs"], parse_mode="Markdown",
                        disable_web_page_preview=True)


@dp.message_handler(commands=["sru", "s", "search"])
async def wikis(message):
    await wikiSearch(message, "ru")


@dp.message_handler(commands=["wikiru",
                              "wikiru2",
                              "wru", "w",
                              "wiki", "wiki2"])
async def wikiru(message):
    await getWiki(message, "ru")


@dp.message_handler(commands=["wikien", "van", "wen", "v"])
async def wikien(message):
    await getWiki(message, "en")


@dp.message_handler(commands=["wikisv", "wsv"])
async def wikisv(message):
    await getWiki(message, "sv")


@dp.message_handler(commands=["wikide", "wde"])
async def wikide(message):
    await getWiki(message, "de")


@dp.message_handler(commands=["wikice", "wce"])
async def wikice(message):
    await getWiki(message, "ce")


@dp.message_handler(commands=["wikitt", "wtt"])
async def wikitt(message):
    await getWiki(message, "tt")


@dp.message_handler(commands=["wikiba", "wba"])
async def wikiba(message):
    await getWiki(message, "ba")


@dp.message_handler(commands=["wikipl", "wpl"])
async def wikipl(message):
    await getWiki(message, "pl")


@dp.message_handler(commands=["wikiua", "wikiuk", "wuk", "wua", "pawuk"])
async def wikiua(message):
    await getWiki(message, "uk")


@dp.message_handler(commands=["wikibe", "wbe",
                              "tarakanwiki",
                              "lukaswiki",
                              "potato",
                              "potatowiki"])
async def wikibe(message):
    await getWiki(message, "be")


@dp.message_handler(commands=["wikies", "wes"])
async def wikies(message):
    await getWiki(message, "es")


@dp.message_handler(commands=["wikihe", "whe"])
async def wikihe(message):
    await getWiki(message, "he")


@dp.message_handler(commands=["wikixh", "wxh"])
async def wikixh(message):
    await getWiki(message, "xh")


@dp.message_handler(commands=["wikiab", "wab"])
async def wikiab(message):
    await getWiki(message, "ab")


@dp.message_handler(commands=["wikibe-tarask", "wikibet", "wbet", "xbet"])
async def wikibet(message):
    await getWiki(message, "be-tarask")


@dp.message_handler(commands=["wiki_usage"])
async def wiki_usage(message):
    await message.reply(data["wiki_query_example"], parse_mode="Markdown")


@dp.message_handler(lambda message: message.text.startswith("/w_"))
async def detect(message):
    text = message.text.replace("/w_", "")
    if text.find("@") != -1:
        text = text.split("@", maxsplit=1)[0]

    w = Wikipya("ru")

    try:
        id_ = int(text)

    except Exception:
        message.reply("id должен быть числом")
        return

    name = await w.getPageName(id_)

    if name == -1:
        await message.reply("Не получилось найти статью по айди")
        return

    await getWiki(message, name=name)
