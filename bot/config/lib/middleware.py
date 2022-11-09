from typing import Any

from aiogram import types
from aiogram.contrib.middlewares.i18n import \
    I18nMiddleware as I18nMiddlewareBase
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from pyi18n_new.models.value import TranslateDict, TranslateList, TranslateStr

from ...schemas import ChatMember, Command, Note


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

        try:
            return self.pyi18n.translate(path=singular, lang=lang, **kwargs)
        except TypeError:
            return singular

    def get_member_locale(self) -> str | None:
        chat = types.Chat.get_current()
        user = types.User.get_current()

        if chat and (chat_lang := Note.get(chat.id, "__chat_lang__")):
            return chat_lang.strip()
        elif user and (user_chat_lang := Note.get(user.id, "__chat_lang__")):
            return user_chat_lang.strip()
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
    async def on_process_message(self, message: types.Message, data):
        command = message.get_command(pure=True)
        args = message.get_args()

        locked_commands = Note.get(message.chat.id, "locked_commands", [], lambda x, default: x.split(" "))

        member = ChatMember.get_by_message(message)

        if command is not None:
            Command.create(
                member_id=member,
                command=command.lower(),
                params=args
            )

        for lcommand_raw in locked_commands:
            lcommand = lcommand_raw.removeprefix("-")
            is_force_admin = command != lcommand_raw

            if command != lcommand:
                continue

            if (not is_force_admin) or (is_force_admin and not await member.check_admin()):
                raise CancelHandler()
