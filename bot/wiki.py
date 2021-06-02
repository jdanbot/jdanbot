from .lib.text import bold, code, cuteCrop, fixWords
from .config import (
    bot, dp, logging, WIKIPYA_BLOCKLIST, _,
    LANGS_LIST, UNIQUE_COMMANDS
)

from aiogram import types
from wikipya.aiowiki import Wikipya, NotFound
from .lib.lurkmore import blocklist


WGR_FLAG = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb" +
    "/8/85/Flag_of_Belarus.svg/1000px-Flag_of_Belarus.svg.png"
)

WRW_FLAG = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb" +
    "/5/50/Flag_of_Belarus_%281918%2C_1991%E2%80%931995%29.svg" +
    "/1000px-Flag_of_Belarus_%281918%2C_1991%E2%80%931995%29.svg.png"
)


# Fandom


@dp.message_handler(commands=["railgun"])
async def railgun(message):
    await wiki(message, "Railgun",
               "https://toarumajutsunoindex.fandom.com/api.php")


@dp.message_handler(commands=["fallout"])
async def fallout(message):
    await wiki(message, "Fallout",
               "https://fallout.fandom.com/ru/api.php")


@dp.message_handler(commands=["kaiser", "kaiserreich"])
async def kaiser(message):
    await wiki(message, "Kaiserreich",
               "https://kaiserreich.fandom.com/ru/api.php",
               lurk=True)


@dp.message_handler(commands=["doom"])
async def doom(message):
    await wiki(message, "DooM", "https://doom.fandom.com/api.php")


# LurkMore
@dp.message_handler(commands=["lurk"])
async def Lurk(message):
    await wiki(message, "Lurkmore",
               "https://ipv6.lurkmo.re/api.php", lurk=True,
               img_blocklist=blocklist["images"])

# Фиксить нада
@dp.message_handler(commands=["absurd"])
async def absurd(message):
    await wiki(message, "Absurdopedia",
               "https://absurdopedia.net/w/api.php", lurk=True)


@dp.message_handler(commands=["mrakopedia"])
async def pizdec(message):
    await wiki(message, "mrakopedia",
               "https://mrakopedia.net/w/api.php",
               host="//mrakopedia.net")


@dp.message_handler(commands=["archwiki"])
async def archwiki(message):
    await wiki(message, "archwiki",
               "https://wiki.archlinux.org/api.php")


@dp.message_handler(commands=["encycl"])
async def encyclopedia(message):
    await wiki(message, "encyclopedia",
               "https://encyclopatia.ru/w/api.php")


# Wikipedia
@dp.message_handler(commands=["wru"])
async def wru(message):
    await wiki(message, "Wiki:RU",
               "https://ru.wikipedia.org/w/api.php",
               version="1.35")


async def wiki(message, fname, url, lang=None, lurk=False,
               img_blocklist=(), query=None, version="1.0",
               host=""):

    w = Wikipya(url=url, lang=lang, version=version,
                img_blocklist=img_blocklist, host=host)

    try:
        if query is None:
            command, query = message.text.split(maxsplit=1)

        page, image, url = await w.get_all(
            query, lurk,
            blocklist=WIKIPYA_BLOCKLIST
        )
        text = fixWords(page.parsed)
    except ValueError:
        await message.reply(
            _("errors.enter_wiki_query").format(message.text),
            parse_mode="Markdown")
        return
    except Exception as e:
        await message.reply(bold(_("errors.error")) + "\n" + code(e),
                            parse_mode="HTML")
        return

    if image != -1:
        await message.reply_photo(
            image, caption=cuteCrop(text, limit=1024),
            parse_mode="HTML")
    else:
        await message.reply(cuteCrop(text, limit=4096),
                            parse_mode="HTML")


async def _wiki(message, fname, url, lang=None, lurk=False,
               img_blocklist=(), name=None, version="1.0"):
    wiki = Wikipya(url=url, lang=lang, version=version,
                   img_blocklist=img_blocklist)
    # wiki = Wikipya(url="https://kaiserreich.fandom.com/ru/api.php")

    if name is None:
        opts = message.text.split(maxsplit=1)
        if len(opts) == 1:
            await message.reply(_("errors.enter_wiki_query").format(opts[0]),
                                parse_mode="Markdown")
            return

        name = opts[1]

    try:
        search = await wiki.search(name)

    except NotFound:
        await message.reply(_("errors.not_found"))
        return

    if lurk:
        opensearch = await wiki.opensearch(name)
        url = "example.com"

        page = await wiki.page(opensearch[0])

    else:
        opensearch = await wiki.opensearch(search[0].title)
        url = opensearch[-1][0]

        page = await wiki.page(search[0])

    page.blockList = WIKIPYA_BLOCKLIST
    text = fixWords(page.parsed)

    try:
        image = await page.image()
        image = image.source

    except Exception as e:
        print(e)
        image = -1

    keyboard = types.InlineKeyboardMarkup()

    try:
        name = search[0].title
    except KeyError:
        name = name

    # url = "https://jdan734.me"

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
            await bot.send_chat_action(message.chat.id, "typing")

            try:
                await message.reply(cuteCrop(text, limit=4096),
                                    parse_mode="HTML",
                                    reply_markup=keyboard)

            except Exception:
                pass
                await message.reply(bold(_("errors.error")) + "\n" + code(e),
                                    parse_mode="HTML")
