from typing import Any

from aiogram import types, BaseMiddleware

from typing import Callable, Dict, Awaitable
from fluentogram import TranslatorHub

from aiogram.filters import Command as CommandFilter
from ...database import Command, Member, Note


class TranslatorRunnerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[
            [types.Message, Dict[str, Any]], Awaitable[Any]
        ],
        event: types.Message,
        data: Dict[str, Any],
    ) -> Any:
        hub: TranslatorHub = data.get("_translator_hub")

        data["user_lang"] = await self.get_language(event)
        data["_"] = hub.get_translator_by_locale(data["user_lang"])

        return await handler(event, data)

    @classmethod
    async def get_language(cls, event: types.Update) -> str:
        if event.inline_query:
            event: types.InlineQuery = event.inline_query
            user_id, check_chat = (
                event.from_user.id,
                False,
            )
        else:
            event: types.Message = event.message

            member = await Member.get_by(event)
            user_id, check_chat = member.user.id, True

        if check_chat and (
            chat_lang := await Note.get(
                member.chat.id, "__chat_lang__"
            )
        ):
            return chat_lang.strip()
        elif user_chat_lang := await Note.get(
            user_id, "__chat_lang__"
        ):
            return user_chat_lang.strip()
        elif user := event.from_user:
            return user.language_code
        else:
            return "ru"


class SpyMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[
            [types.TelegramObject, Dict[str, Any]], Awaitable[Any]
        ],
        message: types.Message,
        data: Dict[str, Any],
    ):
        command_orig = CommandFilter.extract_command(
            self=CommandFilter, text=message.text
        )

        command = command_orig.command
        args = command_orig.args

        locked_commands = await Note.get(
            message.chat.id,
            "locked_commands",
            [],
            lambda x, default: x.split(" "),
        )

        if command is not None:
            member = await Member.get_by(message)

            await Command(
                user_id=member.user.id,
                chat_id=member.chat.id,
                name=command.lower(),
                args=args,
            ).insert()

        for lcommand_raw in locked_commands:
            lcommand = lcommand_raw.removeprefix("-")
            is_force_admin = command != lcommand_raw

            if command != lcommand:
                continue

            if (not is_force_admin) or (
                is_force_admin and not await member.check_admin()
            ):
                return

        await handler(message, data)
