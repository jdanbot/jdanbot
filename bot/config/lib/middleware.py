from typing import Any
from ...schemas import Note, Command, ChatMember

from aiogram.contrib.middlewares.i18n import I18nMiddleware as I18nMiddlewareBase
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types


from pyi18n_new.models.value import TranslateStr, TranslateDict, TranslateList


class I18nMiddleware(I18nMiddlewareBase):
    def t(
        self,
        singular: str,
        plural: str = None,
        n: int = 1,
        locale: str = None,
        return_lang: bool = False,
        force_reload: bool = False,
        **kwargs
    ) -> TranslateStr | TranslateList | TranslateDict:
        # TODO: Research locale argument

        if force_reload:
            self.ctx_locale.set(self.get_member_locale())

        lang = self.ctx_locale.get()
        lang = "uk" if lang == "ua" else lang

        if lang is None or lang not in ("uk", "en", "ru"):
            lang = "ru"

        if return_lang:
            return lang

        return self.pyi18n.translate(path=singular, lang=lang, **kwargs)

    def get_member_locale(self) -> str | None:
        chat = types.Chat.get_current()
        user = types.User.get_current()

        if chat and (chat_lang := Note.get(chat.id, "__chat_lang__")):
            return chat_lang
        elif user and (user_chat_lang := Note.get(user.id, "__chat_lang__")):
            return user_chat_lang
        elif user:
            return user.language_code
        else:
            return None

    async def get_user_locale(
        self,
        action: str | None = None,
        args: tuple[Any] = None
    ) -> str | None:
        return self.get_member_locale()


class SpyMiddleware(BaseMiddleware):
    async def on_process_message(self, message, data):
        command = message.get_full_command()

        if command is not None:
            Command.create(
                member_id=ChatMember.get_by_message(message),
                command=command[0][1:].split("@")[0].lower(),
                params=command[1]
            )
