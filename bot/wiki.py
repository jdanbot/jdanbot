from .lib.text import bold, code, cuteCrop, fixWords
from .config import (
    bot, dp, logging, WIKIPYA_BLOCKLIST, _,
    LANGS_LIST, UNIQUE_COMMANDS
)

from aiogram import types
from wikipya.aiowiki import Wikipya, NotFound

import yaml
from bs4 import BeautifulSoup
from tghtml import TgHTML


with open("bot/lib/blocklist.yml") as file:
    blocklist = yaml.safe_load(file.read())


@dp.message_handler(commands=["railgun"])
async def railgun(message):
    await wiki(message, "Railgun",
               "https://toarumajutsunoindex.fandom.com/api.php",
               lurk=True)


@dp.message_handler(commands=["fallout"])
async def fallout(message):
    await wiki(message, "Fallout",
               "https://fallout.fandom.com/ru/api.php", lurk=True)


@dp.message_handler(commands=["kaiser", "kaiserreich"])
async def kaiser(message):
    await wiki(message, "Kaiserreich",
               "https://kaiserreich.fandom.com/ru/api.php",
               lurk=True)


@dp.message_handler(commands=["doom"])
async def doom(message):
    await wiki(message, "DooM", "https://doom.fandom.com/api.php",
               lurk=True)


@dp.message_handler(commands=["lurk"])
async def Lurk(message):
    await wiki(message, "Lurkmore",
               "https://ipv6.lurkmo.re/api.php", lurk=True,
               prefix="",
               img_blocklist=blocklist["images"])


@dp.message_handler(commands=["absurd"])
async def absurd(message):
    await wiki(message, "Absurdopedia",
               "https://absurdopedia.net/w/api.php", lurk=True,
               prefix="/wiki")


@dp.message_handler(commands=["mrakopedia", "pizdec"])
async def pizdec(message):
    await wiki(message, "mrakopedia",
               "https://mrakopedia.net/w/api.php",
               host="//mrakopedia.net", prefix="/wiki")


@dp.message_handler(commands=["archwiki"])
async def archwiki(message):
    await wiki(message, "archwiki",
               "https://wiki.archlinux.org/api.php")


@dp.message_handler(commands=["encycl"])
async def encyclopedia(message):
    await wiki(message, "encyclopedia",
               "https://encyclopatia.ru/w/api.php", lurk=True,
               host="//encyclopatia.ru", prefix="/wiki")


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
        await wiki(message, "Wiki",
                   "https://{lang}.wikipedia.org/w/api.php", lang=lang,
                   version="1.35")
        return

    else:
        for lang in UNIQUE_COMMANDS:
            if command[1:] in UNIQUE_COMMANDS[lang]:
                await wiki(message, "Wiki",
                           "https://{lang}.wikipedia.org/w/api.php",
                           version="1.35", lang=lang)
                break


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

    await wiki(message, lang="ru", name=name)


async def wiki(message, fname, url, query=None, lang=None,
               lurk=False, **kwargs):
    w = Wikipya(url=url, lang=lang, **kwargs)

    try:
        if query is None:
            command, query = message.text.split(maxsplit=1)

        page, image, url = await w.get_all(
            query, lurk,
            blocklist=WIKIPYA_BLOCKLIST
        )
        text = fixWords(page.parsed)

    except NotFound:
        await message.reply(_("errors.not_found"))
        return

    except ValueError:
        await message.reply(
            _("errors.enter_wiki_query").format(message.text),
            parse_mode="Markdown")
        return

    except Exception as e:
        await message.reply(bold(_("errors.error")) + "\n" + code(e),
                            parse_mode="HTML")
        return

    soup = BeautifulSoup(text, "lxml")

    i = soup.find_all("i")
    b = soup.find_all("b")

    if len(i) != 0:
        i[0].unwrap()

    if len(b) != 0:
        if url is not None:
            b = b[0]
            b.name = "a"
            b["href"] = url
            b = b.wrap(soup.new_tag("b"))

    text = unbody(soup)

    try:
        if image != -1:
            cropped = cuteCrop(text, limit=1024)

            if cropped == "":
                cropped = text[:1024]

            await message.reply_photo(
                image, caption=cropped,
                parse_mode="HTML")
        else:
            await message.reply(
                cuteCrop(text, limit=4096),
                parse_mode="HTML",
                disable_web_page_preview=True
            )

    except Exception as e:
        await message.reply(bold(_("errors.error")) + "\n" + code(e),
                            parse_mode="HTML")
        await message.answer(cuteCrop(text, limit=4096),
                             disable_web_page_preview=True)


def unbody(html):
    return str(html).replace("<p>", "").replace("</p>", "") \
                    .replace("<html><body>", "") \
                    .replace("</body></html>", "")
