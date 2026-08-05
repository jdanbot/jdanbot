from collections.abc import Awaitable
from typing import Any, Callable, override

from aiogram import BaseMiddleware, types

from ...database import Chat
from .locales import locales


class i18nMiddleware(BaseMiddleware):
    @override
    async def __call__(
        self,
        handler: Callable[
            [types.TelegramObject, dict[str, Any]],
            Awaitable[Any],
        ],
        event: types.TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        data["user_lang"] = await self.detect_language(
            data.get("event_chat"),
            data.get("event_from_user"),
        )

        data["_"] = getattr(
            locales, data["user_lang"], locales.ru
        )

        return await handler(event, data)

    @classmethod
    async def detect_language(
        cls,
        chat: types.Chat | None,
        user: types.User | None,
    ) -> str:
        if chat and (
            chat_lang := await Chat.get_language(chat.id)
        ):
            return chat_lang.strip()
        elif user and (
            user_lang := await Chat.get_language(user.id)
        ):
            return user_lang.strip()
        elif user:
            return user.language_code or "ru"
        else:
            return "ru"
