from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as Button

from wikipya import Wikipya, NotFound
from bs4 import BeautifulSoup
from tghtml import TgHTML


from ..lib import handlers
from ..lib.text import bold, code, cuteCrop, fixWords
from ..config import (
    bot, dp, WIKICOMMANDS, _, LANGS_LIST, UNIQUE_COMMANDS
)


def sort_kb(buttons, row_line=2):
    keyboard = InlineKeyboardMarkup()

    for ind, __ in enumerate(buttons):
        a = buttons[ind:ind + row_line]

        try:
            for i in range(1, row_line if len(buttons) > row_line else len(buttons)):
                buttons.remove(a[i])
        except IndexError:
            pass

        keyboard.add(*a)

    return keyboard


@dp.message_handler(commands=["wiki2"])
@handlers.wikipya_handler
def wiki():
    return Wikipya("ru")


@dp.message_handler(commands=["railgun"])
async def railgun(message):
    await wiki(message, "Railgun",
               "https://toarumajutsunoindex.fandom.com/api.php",
               is_lurk=True)


@dp.message_handler(commands=["fallout"])
async def fallout(message):
    await wiki(message, "Fallout",
               "https://fallout.fandom.com/ru/api.php", is_lurk=True, prefix="")


@dp.message_handler(commands=["kaiser", "kaiserreich"])
async def kaiser(message):
    await wiki(message, "Kaiserreich",
               "https://kaiserreich.fandom.com/ru/api.php",
               is_lurk=True)


@dp.message_handler(commands=["doom"])
async def doom(message):
    await wiki(message, "DooM", "https://doom.fandom.com/api.php",
               is_lurk=True)


@dp.message_handler(commands=["lurk"])
async def Lurk(message):
    await wiki(message, "Lurkmore",
               "http://lurkmore.to/api.php",
               prefix="",
               is_lurk=True)


@dp.message_handler(commands=["absurd"])
async def absurd(message):
    await wiki(message, "Absurdopedia",
               "https://absurdopedia.net/w/api.php", is_lurk=True,
               prefix="/wiki")


@dp.message_handler(commands=["mrakopedia", "pizdec"])
async def pizdec(message):
    await wiki(message, "mrakopedia",
               "https://mrakopedia.net/w/api.php",
               host="//mrakopedia.net", is_lurk=True, prefix="/wiki")


@dp.message_handler(commands=["archwiki"])
async def archwiki(message):
    await wiki(message, "archwiki", is_lurk=True,
               base_url="https://wiki.archlinux.org/api.php")


@dp.message_handler(commands=["encycl"])
async def encyclopedia(message):
    await wiki(message, "encyclopedia",
               "https://encyclopatia.ru/w/api.php", is_lurk=True,
               host="//encyclopatia.ru", prefix="/wiki")


@dp.message_handler(commands=["langs", "wikilangs", "wiki_langs"])
async def getLangs(message):
    await message.reply(_("wiki.langs"), parse_mode="Markdown",
                        disable_web_page_preview=True)


@dp.message_handler(commands=WIKICOMMANDS)
async def wikihandler(message):
    command = message.text.split()[0]
    lang = command.replace("/wiki", "") \
                  .replace("/w", "")

    for lang_ in UNIQUE_COMMANDS:
        if command[1:] in UNIQUE_COMMANDS[lang_]:
            lang = lang_
            break

    if lang not in LANGS_LIST:
        return

    await wiki(message, "Wiki",
               "https://{lang}.wikipedia.org/w/api.php", lang=lang)


@dp.message_handler(lambda message: message.text.startswith("/w_"))
async def detect(message):
    text = message.text.replace("/w_", "")
    if text.find("@") != -1:
        text = text.split("@", maxsplit=1)[0]

    w = Wikipya("ru").get_instance()

    try:
        id_ = int(text)

    except Exception:
        message.reply(_("errors.invalid_post_id"))
        return

    name = await w.get_page_name(id_)

    if name == -1:
        await message.reply(_("errors.not_found"))
        return

    await wiki(message, "wikipedia", lang="ru", query=name)


async def wiki(message, fname, base_url="https://{lang}.wikipedia.org/w/api.php",
               query=None, lang=None, is_lurk=False, prefix="w", **kwargs):
    w = Wikipya(base_url=base_url, lang=lang, is_lurk=is_lurk,
                prefix=prefix, **kwargs).get_instance()

    try:
        if query is None:
            command, query = message.text.split(maxsplit=1)

        page, image, url = await w.get_all(query, is_lurk, get_full_page=False)
        text = fixWords(page.text)

    except NotFound:
        await message.reply(_("errors.not_found"))
        return

    except ValueError:
        await message.reply(
            _("errors.enter_wiki_query").format(message.text),
            parse_mode="Markdown")
        return

    # sections = await w.sections(page.title)
    # buttons = [Button("Главная", callback_data=f"{sections.pageid} 0")]

    # for section in sections.sections:
    #     buttons.append(Button(section.title, callback_data=f"{sections.pageid} {section.number}"))

    # kb = sort_kb(buttons, row_line=3)

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

            await bot.send_chat_action(message.chat.id, "upload_photo")
            await message.reply_photo(
                image, caption=cropped,
                parse_mode="HTML")
        else:
            await message.reply(
                cuteCrop(text, limit=4096),
                parse_mode="HTML",
                disable_web_page_preview=True,
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


@dp.message_handler(commands="s")
async def wikiSearch(message, lang="ru"):
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


@dp.message_handler(commands="wtest")
@handlers.get_text
async def wikiSummary(message, query):
    wiki = Wikipya(lang="ru").get_instance()

    res = await wiki.summary(query)

    if res.original_image:
        cropped = cuteCrop(str(TgHTML(res.extract_html)), limit=1024)

        if cropped == "":
            cropped = str(TgHTML(res.extract_html))[:1024]

        await bot.send_chat_action(message.chat.id, "upload_photo")
        await message.reply_photo(
            res.original_image.source, caption=cropped,
            parse_mode="HTML")
    else:
        await message.reply(
            cuteCrop(str(TgHTML(res.extract_html)), limit=4096),
            parse_mode="HTML",
            disable_web_page_preview=True
        )
