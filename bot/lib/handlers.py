from ..config import dp, bot, Note, _

from .admin import check_admin
from .models import Article

from random import randint

from aiogram import types
from aiogram.types import InlineKeyboardButton as Button
from bs4 import BeautifulSoup

from wikipya.clients import MediaWiki
from wikipya import models


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


def randomed_start(func):
    async def wrapper(message):
        if randint(0, 1) == 0:
            await func(message)

    return wrapper


def parse_arguments(limit, without_params=False):
    def argument_wrapper(func):
        async def wrapper(message):
            try:
                params = message.get_full_command()[1].split(maxsplit=limit - 1)
            except AttributeError:
                params_raw = message.data.split()
                params = " ".join(params_raw[1:-1]).split(maxsplit=limit - 1)
                params.append(int(params_raw[-1]))

                message = message.message

            if len(params) < limit and not without_params:
                await message.reply(
                    _("errors.few_args", num=limit), parse_mode="Markdown"
                )
            else:
                return await func(message, *params)

        return wrapper

    return argument_wrapper


def check(var, without_params=False):
    def argument_wrapper(func):
        async def wrapper(message):
            res = Note.get(message.chat.id, var)

            if res is None:
                res = "True"

            if str(res).title() == "True":
                await func(message)

        return wrapper

    return argument_wrapper


def get_text(func):
    @parse_arguments(1, without_params=True)
    async def wrapper(message, query=None):
        reply = message.reply_to_message

        if reply and reply.text:
            text = reply.text
        elif reply and reply.caption:
            text = reply.caption
        elif query:
            text = query
        else:
            await message.reply(_("errors.few_args", num=1), parse_mode="Markdown")
            return

        return await func(message, text)

    return wrapper


def only_jdan(func):
    async def wrapper(message):
        if message.from_user.id == 795449748:
            await func(message)

    return wrapper


def only_admins(func):
    async def wrapper(message):
        if message.chat.type == "supergroup" and await check_admin(message, bot):
            await func(message)

    return wrapper


def sections_to_keyboard(
    sections: list[models.Section],
    active_section: int,
    prefix: str
) -> types.InlineKeyboardMarkup:
    buttons = [Button(
        f"✅ {section.number}. {section.title}" if active_section == section.index
        else f"{section.number}. {section.title}",
        callback_data=f"{prefix} {section.from_title} {section.index}"
    ) for section in sections]

    buttons.insert(0, Button(
        f"✅ {sections[0].from_title}" if active_section == 0 else sections[0].from_title,
        callback_data=f"{prefix} {sections[0].from_title} 0")
    )

    return sort_kb(buttons)


def wikipya_handler(*prefix):
    def argument_wrapper(func):
        @dp.message_handler(commands=prefix)
        @dp.callback_query_handler(lambda x: x.data.startswith(f"{prefix[0]} "))
        @send_article
        @parse_arguments(1, without_params=True)
        async def wrapper(message: types.Message, query: str, section: int = 0) -> Article:
            wiki: MediaWiki = (await func(message)).get_instance()

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
                        b["href"] = image if image != -1 else url
                        b = b.wrap(soup.new_tag("b"))

                text = unbody(soup)
            else:
                page = await wiki.page(query, section=section)

                text = page.parsed
                image = -1

            sections = (await wiki.sections(page.title)).sections

            image = -1

            return Article(
                text,
                keyboard=sections_to_keyboard(sections, section, prefix[0])
            )

        return wrapper
    return argument_wrapper


def send_article(func):
    async def wrapper(message: types.Message, *args):
        result = await func(message, *args)

        if result.image:
            await message.answer_chat_action("upload_photo")
            await message.reply_photo(
                result.image,
                caption=result.text,
                parse_mode="HTML",
                reply_markup=result.keyboard,
            )
        else:
            if str(type(message)) == "<class 'aiogram.types.callback_query.CallbackQuery'>":
                message = message.message
                message.reply = message.edit_text

            await message.reply(
                result.text,
                parse_mode="HTML",
                disable_web_page_preview=False,
                reply_markup=result.keyboard,
            )

    return wrapper


def unbody(html):
    return str(html).replace("<p>", "").replace("</p>", "") \
                    .replace("<html><body>", "") \
                    .replace("</body></html>", "")
