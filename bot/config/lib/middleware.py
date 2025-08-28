from typing import Any, Awaitable, Callable, Dict, override

from aiogram import BaseMiddleware, types
from aiogram.filters import Command as CommandFilter

from ...database import Command, Member
from .locales import locales


class TranslatorRunnerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[
            [types.Message, Dict[str, Any]], Awaitable[Any]
        ],
        event: types.Message,
        data: Dict[str, Any],
    ) -> Any:
        data["user_lang"] = await self.get_language(event)

        try:
            data["_"] = getattr(locales, data["user_lang"])
        except KeyError:
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


class SpyMiddleware(BaseMiddleware):
    @override
    async def __call__(
        self,
        handler: Callable[
            [types.TelegramObject, Dict[str, Any]],
            Awaitable[Any],
        ],
        message: types.Message,
        data: Dict[str, Any],
    ):
        command_orig = CommandFilter.extract_command(
            self=CommandFilter, text=message.text
        )

        command = command_orig.command
        args = command_orig.args

        member = await Member.get_by(message)

        locked_commands = (
            await Member.get_note("locked_commands") or ""
        ).split(" ")

        if command is not None:
            member = await Member.get_by(message)
            data["member"] = member

            await Command(
                user_id=member.user_id,
                chat_id=member.chat_id,
                name=command.lower(),
                args=args or "",
            ).save()

        for lcommand_raw in locked_commands:
            lcommand = lcommand_raw.removeprefix("-")
            is_force_admin = command != lcommand_raw

            if command != lcommand:
                continue

            if (not is_force_admin) or (
                is_force_admin
                and not await member.check_admin()
            ):
                return

        await handler(message, data)
