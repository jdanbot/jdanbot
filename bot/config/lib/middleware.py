import os

import yaml
import i18n

from .text import fixHTML
from ..database import notes, command_stats

from aiogram.contrib.middlewares.i18n import I18nMiddleware as I18nMiddlewareBase
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types


class I18nMiddleware(I18nMiddlewareBase):
    def t(self, singular, plural=None, n=1, locale=None,
          enable_patch=False, prepare_kwargs=False, **kwargs):
        self.i18n = i18n
        self.i18n.load_path.append(self.path)

        res = self.gettext(singular, plural, n, locale)

        lang = self.ctx_locale.get()
        lang = "uk" if lang == "ua" else lang

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

                elif isinstance(translate, dict):
                    return translate

                return [[__.format(**kwargs) for __ in translate] if isinstance(_, list)
                        else _.format(**kwargs) for _ in translate]


    async def get_user_locale(self, action: str, args: None):
        user = types.User.get_current()
        chat = types.Chat.get_current()

        chat_locale = await notes.get(chat.id, "__chat_lang__")
        locale = user.locale if user else None

        if locale:
            *_, data = args
            language = data["locale"] = locale.language
            return chat_locale or language

        return None


class SpyMiddleware(BaseMiddleware):
    async def on_process_message(self, message, data):
        command = message.get_full_command()

        if command is not None:
            await command_stats.insert(
                message.chat.id, message.from_user.id,
                command[0][1:]
            )
            await command_stats._conn.commit()


