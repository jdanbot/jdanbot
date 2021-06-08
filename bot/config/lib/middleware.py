import os, sys

import yaml
import i18n
import asyncio
from unsync import unsync

from .text import fixHTML
from ..database import notes, command_stats, events

from aiogram.contrib.middlewares.i18n import I18nMiddleware as I18nMiddlewareBase
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram import types, Dispatcher
from aiogram.utils.exceptions import Throttled


@unsync
async def get_chat_locale(chat):
    return None if chat is None else await notes.get(
        chat.id,
        "__chat_lang__"
    )


class I18nMiddleware(I18nMiddlewareBase):
    def t(self, singular, plural=None, n=1, locale=None,
          enable_patch=False, prepare_kwargs=False, **kwargs):
        self.i18n = i18n
        self.i18n.load_path.append(self.path)

        res = self.gettext(singular, plural, n, locale)

        chat = types.Chat.get_current()
        chat_lang = get_chat_locale(chat).result()

        user_lang = self.ctx_locale.get()

        lang = chat_lang or user_lang or self.default
        lang = "uk" if lang == "ua" else lang

        lang = "en"

        self.i18n.set("locale", lang)
        self.i18n.set("fallback", self.default)

        if prepare_kwargs:
            for arg in kwargs:
                kwargs[arg] = fixHTML(kwargs[arg])

        try:
            if enable_patch:
                raise TypeError

            return self.i18n.t(res, **kwargs)
        except TypeError:
            path = f"{self.path}/{res.split('.')[0]}.{{lang}}.yml"

            if not os.path.exists(path.format(lang=lang)):
                lang = self.default

            with open(path.format(lang=lang),
                      encoding="UTF-8") as f:
                locale = yaml.safe_load(f.read())
                translate = locale.get(lang).get(res.split(".")[1])

                if isinstance(translate, str):
                    return translate.format(**kwargs)

                return [_.format(**kwargs) if isinstance(_, list) else _.format(**kwargs)
                        for _ in translate]


class SpyMiddleware(BaseMiddleware):
    async def on_process_message(self, message, data):
        command = message.get_full_command()

        await self.reg_user_in_db(message)

        if command is None:
            return
        else:
            await command_stats.insert(
                message.chat.id, message.from_user.id,
                command[0][1:]
            )
            await command_stats._conn.commit()

    async def reg_user_in_db(self, message):
        user = message.from_user
        cur_user = await events.select(where=[
            events.id == user.id,
            events.chatid == message.chat.id
        ])

        if len(cur_user) == 0:
            await events.insert(message.chat.id, user.id, user.full_name)
            await events.conn.commit()
