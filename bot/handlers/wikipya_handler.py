import urllib

from aiogram import types
from aiogram.types import InlineKeyboardButton as Button
from aiogram.utils.markdown import hide_link
from bs4 import BeautifulSoup

from ..config import dp

from ..lib.models import Article

from wikipya import models
from wikipya.clients import MediaWiki

from .send_article import send_article
from .parse_arguments import parse_arguments


def sort_kb(buttons: list[Button], row_line: int = 2) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()

    for ind, __ in enumerate(buttons):
        a = buttons[ind:ind + row_line]

        try:
            for i in range(1, row_line if len(buttons) > row_line else len(buttons)):
                buttons.remove(a[i])
        except IndexError:
            pass

        keyboard.add(*a)

    return keyboard



def unbody(html):
    return str(html).replace("<p>", "").replace("</p>", "") \
                    .replace("<html><body>", "") \
                    .replace("</body></html>", "")


def wikipya_handler(
    *prefix,
    extract_query_from_url=False,
    enable_experemental_navigation=False,
    went_trigger_command=False
):
    def argument_wrapper(func):
        @dp.message_handler(commands=prefix)
        @dp.callback_query_handler(lambda x: x.data.startswith(f"{prefix[0]} "))
        @send_article
        @parse_arguments(1, without_params=True)
        async def wrapper(message: types.Message, query: str, section: int = 0) -> Article:
            if extract_query_from_url:
                url = query.split("/")
                query = url[-1]

            answer = (message, message.text) if went_trigger_command else (message,)

            try:
                wiki, *__ = await func(*answer)
                wiki: MediaWiki = wiki.get_instance()

                section = __[0] if len(__) > 0 else section
            except:
                wiki: MediaWiki = (await func(*answer)).get_instance()

            query = query.split("#")[0]

            query = urllib.parse.unquote(query, encoding='utf-8', 
                                     errors='replace').replace("_", " ")

            if query.startswith("id"):
                page_id = int(query.removeprefix("id"))
                query = await wiki.get_page_name(page_id)

            if section == 0:
                page, image, url = await wiki.get_all(query)

                soup = BeautifulSoup(page.parsed, "lxml")

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

                text = hide_link(image) + unbody(soup)

            else:
                search = await wiki.search(query)
                page = await wiki.page(search[0].title, section=section)

                url = "https://example.org"

                text = page.parsed
                image = -1

            sections = (await wiki.sections(page.title)).sections

            raw_image = image
            image = -1

            if enable_experemental_navigation:
                kb = sections_to_keyboard(sections, section, prefix[0])
                kb = types.InlineKeyboardMarkup()
            else:
                kb = types.InlineKeyboardMarkup()

            if enable_experemental_navigation:
                kb.inline_keyboard.insert(0, [Button("test", callback_data=f"test {prefix[0]} {section} {query}")])

            # if url:
            #     kb.inline_keyboard.insert(0, [Button(_("wiki.read_full"), url)])

            return Article(
                text,
                keyboard=kb,
                disable_web_page_preview=raw_image == -1
            )

        return wrapper
    return argument_wrapper


@dp.callback_query_handler(lambda x: x.data.startswith("test "))
async def test(call: types.CallbackQuery):
    await call.answer()
    _, prefix, section, query = call.data.split(" ", maxsplit=3)

    from wikipya import Wikipya

    # how get instance from query?
    wiki = Wikipya(base_url="https://ru.wikipedia.org/w/api.php").get_instance()

    print(len(call.message.reply_markup.inline_keyboard))

    if len(call.message.reply_markup.inline_keyboard) == 1:
        sections = (await wiki.sections(query)).sections
        kb = sections_to_keyboard(sections, section, prefix)
        kb.inline_keyboard.insert(0, [Button("test", callback_data=f"test {prefix} {section} {query}")])
    else:
        kb = types.InlineKeyboardMarkup()
        kb.add(Button("test", callback_data=f"test {prefix} {section} {query}"))

    await call.message.edit_reply_markup(kb)


def sections_to_keyboard(
    sections: list[models.Section],
    active_section: int,
    prefix: str
) -> types.InlineKeyboardMarkup:
    buttons = [Button(
        f"✅ {section.number}. {section.title}" if int(active_section) == section.index
        else f"{section.number}. {section.title}",
        callback_data=f"{prefix} {section.from_title} {section.index}"
    ) for section in sections]

    buttons.insert(0, Button(
        f"✅ {sections[0].from_title.replace('_', ' ')}" if int(active_section) == 0
        else sections[0].from_title.replace("_", " "),
        callback_data=f"{prefix} {sections[0].from_title} 0")
    )

    return sort_kb(buttons)
