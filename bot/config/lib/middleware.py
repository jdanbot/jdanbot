import os
import yaml

from dataclasses import dataclass

from ..database import Note, Command, ChatMember

from aiogram.contrib.middlewares.i18n import I18nMiddleware as I18nMiddlewareBase
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types


@dataclass
class Locale:
    name: str = "None"
    lang: str = None

    def load(self, path):
        self.locale = {}

        for file in os.listdir(path):
            name, lang, ext = file.split(".", maxsplit=2)

            if lang != self.lang:
                continue

            with open(f"{path}/{file}", encoding="UTF-8") as f:
                self.locale[name] = yaml.safe_load(
                    f.read().replace("%{", "{"))[lang]


class I18nMiddleware(I18nMiddlewareBase):
    def find_locales(self):
        locales = {}

        for name in os.listdir(self.path):
            lang = name.split(".", maxsplit=2)[1]

            if locales.get(lang) is None:
                locales[lang] = Locale(lang=lang)
                locales[lang].load(self.path)

        return locales

    def t(self, singular, plural=None, n=1, locale=None, **kwargs):
        lang = self.ctx_locale.get()
        lang = "uk" if lang == "ua" else lang

        section, name = singular.split(".", maxsplit=1)

        if lang is None or lang not in set(self.locales):
            lang = "ru"

        translate = self.locales[lang].locale[section]
        n_ = name.split(".", maxsplit=1)

        if len(n_) > 1:
            name, post = n_
            translate = translate[name][post]
        else:
            translate = translate[name]

        if isinstance(translate, str):
            if len(kwargs.items()) != 0:
                return translate.format(**kwargs)
            else:
                return translate

        elif isinstance(translate, dict):
            try:
                count = kwargs["count"]

                if count == 0:
                    value = "zero"
                elif count == 1:
                    value = "one"
                elif count in (2, 3, 4, 5):
                    value = "few"
                else:
                    value = "many"

                return translate[value].format(**kwargs)
            except:
                pass

            for key in translate:
                if isinstance(translate[key], (dict, list)):
                    return translate

                translate[key] = translate[key].format(**kwargs)

            return translate

        elif isinstance(translate, list):
            trans = []

            for item in translate:
                if isinstance(item, (dict, list)):
                    trans.append(translate)
                else:
                    trans.append(item.format(**kwargs))

            return trans

    async def get_user_locale(self, action: str = None, args: None = None):
        user = types.User.get_current()
        chat = types.Chat.get_current()

        locale = user.locale if user else None
        chat_locale = Note.get(
            chat.id,
            "__chat_lang__"
        ) if chat is not None else None

        if locale:
            # *_, data = args
            # language = data["locale"] = locale.language
            return chat_locale or locale.language

        return None


class SpyMiddleware(BaseMiddleware):
    async def on_process_message(self, message, data):
        command = message.get_full_command()

        if command is not None:
            Command.create(
                member_id=ChatMember.get_by_message(message),
                command=command[0][1:].split("@")[0].lower(),
                params=command[1]
            )
