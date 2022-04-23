import os

from ..database import Note, Command, ChatMember

from aiogram.contrib.middlewares.i18n import I18nMiddleware as I18nMiddlewareBase
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types


class I18nMiddleware(I18nMiddlewareBase):
    def t(self, singular, plural=None, n=1, locale=None, **kwargs):
        lang = self.ctx_locale.get()
        lang = "uk" if lang == "ua" else lang

        section, name = singular.split(".", maxsplit=1)

        if lang is None or lang not in ("uk", "en", "ru"):
            lang = "ru"

        translate = self.pyi18n[lang][section][name]
        if isinstance(translate, dict):
            return translate
        else:
            return translate(**kwargs)

    async def get_user_locale(self, action = None, args = None):
        user = types.User.get_current()
        chat = types.Chat.get_current()

        locale = user.locale if user else None
        chat_locale = Note.get(
            chat.id,
            "__chat_lang__"
        ) if chat is not None else None

        if locale:
            language = locale.language
            return chat_locale or language

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
