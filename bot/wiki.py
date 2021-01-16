from .lib.fixWords import fixWords
from tghtml import tghtml
from .lib.html import bold
from .data import data
from .bot import bot, dp


import aiogram

from wikipya.aiowiki import Wikipya


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

    for prop in r:
        text += bold(fixWords(prop[0])) + "\n"
        text += f"└─/w_{prop[1]}\n"

    await message.reply(text, parse_mode="HTML")


async def getWiki(message=None, lang="ru", logs=False, name=None):
    wiki = Wikipya(lang)

    if name is None:
        opts = message.text.split(maxsplit=1)
        if len(opts) == 1:
            await message.reply(data["wikierror"].format(opts[0]),
                                parse_mode="Markdown")
            return

        query = opts[1]

        print(f"[Wikipedia {lang.upper()}] {query}")

        search = await wiki.search(query)

        if search == -1:
            await message.reply("Ничего не найдено")
            return

        name = search[0][0]
        opensearch = await wiki.opensearch(name)
        url = opensearch[-1][0]

    else:
        print(f"[Wikipedia {lang.upper()}] {name}")

    page = await wiki.getPage(name)

    if page == -1:
        text = ""

    elif str(page) == "":
        text = ""

    else:
        for span in page.find_all("span"):
            span.name = "p"

        for p in page.find_all("p"):
            if p.text == "":
                p.replace_with("")

        text = fixWords(tghtml(str(page)))

    image = await wiki.getImageByPageName(name)

    try:
        image = image.source
    except TypeError:
        pass

    keyboard = aiogram.types.InlineKeyboardMarkup()

    try:
        name = search[0][0]
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
            await message.reply(text, parse_mode="HTML", reply_markup=keyboard)

        except Exception:
            pass

    else:
        if image == data["belarus_flag"]["old"]:
            image = data["belarus_flag"]["new"]

        await bot.send_chat_action(message.chat.id, "upload_photo")

        try:
            await message.reply_photo(image, caption=text,
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

    name = await w.getPageNameById(id_)

    if name == -1:
        await message.reply("Не получилось найти статью по айди")
        return

    await getWiki(message, name=name)
