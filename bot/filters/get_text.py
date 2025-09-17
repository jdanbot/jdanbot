from dataclasses import dataclass

from aiogram import types
from aiogram.filters import BaseFilter, CommandObject
from aiogram.utils.markdown import bold

from ..config import Locale


@dataclass
class GetText(BaseFilter):
    disable_reply: bool = False

    async def __call__(
        self,
        message: types.Message,
        command: CommandObject,
        _: Locale,
    ) -> bool | dict[str, str]:
        reply = message.reply_to_message
        docs = _.docs.get(command.command)

        if command.args:
            text = command.args
        elif message.quote and message.quote.is_manual:
            text = message.quote.text
        elif self.disable_reply:
            await message.reply(
                docs
                or bold(_.errors.command_requires.text),
                parse_mode="markdown",
                disable_web_page_preview=True,
            )

            return False
        elif reply and reply.text:
            text = reply.text
        elif reply and reply.caption:
            text = reply.caption
        elif docs:
            await message.reply(
                docs,
                parse_mode="markdown",
                disable_web_page_preview=True,
            )

            return False
        else:
            await message.reply(
                _.errors.few_args(num=1),
                parse_mode="Markdown",
            )

            return False

        return {"query": text}
