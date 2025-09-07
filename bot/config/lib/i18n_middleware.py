from collections.abc import Awaitable
from typing import Any, Callable, override

from aiogram import BaseMiddleware, types

from ...database import Member
from .locales import locales


class i18nMiddleware(BaseMiddleware):
    @override
    async def __call__(
        self,
        handler: Callable[
            [types.Message, dict[str, Any]], Awaitable[Any]
        ],
        event: types.Message,
        data: dict[str, Any],
    ) -> Any:
        data["user_lang"] = await self.get_language(event)

        # try:
        #     data["_"] = getattr(locales, data["user_lang"])
        # except KeyError:
        data["_"] = locales.ru

        return await handler(event, data)

    @classmethod
    async def get_language(cls, event: types.Update) -> str:
        # print(event.model_dump_json(indent=4))

        try:
            skip_to_message = event.callback_query
            if_has_callback = bool(event.callback_query)
        except Exception:
            skip_to_message = True
            if_has_callback = False

        if if_has_callback:
            event: types.CallbackQuery = (
                event.callback_query
            )

        if not skip_to_message and event.inline_query:
            event: types.InlineQuery = event.inline_query
            user_id, check_chat = (
                event.from_user.id,
                False,
            )
        elif (
            not skip_to_message
            and event.chosen_inline_result
        ):
            event: types.ChosenInlineResult = (
                event.chosen_inline_result
            )
            user_id, check_chat = event.from_user.id, False
        else:
            try:
                event: types.Message = event.message
            except Exception:
                pass

            if event is None:
                return "ru"

            member = await Member.get_by(event)
            user_id, check_chat = member.user_id, True

        if check_chat and (chat_lang := member.lang):
            return chat_lang.strip()
        elif user_chat_lang := await Member.get_note(
            "__chat_lang__"
        ):
            return user_chat_lang.strip()
        elif user := event.from_user:
            return user.language_code
        else:
            return "ru"
