from dataclasses import dataclass
from typing import Dict, Union

from aiogram import types
from aiogram.filters import BaseFilter, CommandObject

from ..config import Locale


@dataclass
class GetText(BaseFilter):
    disable_reply: bool = False

    async def __call__(
        self,
        message: types.Message,
        command: CommandObject,
        _: Locale,
    ) -> Union[bool, Dict[str, str]]:
        reply = message.reply_to_message

        if command.args:
            text = command.args
        elif message.quote and message.quote.is_manual:
            text = message.quote.text
        elif self.disable_reply:
            await message.reply("_.errors.please.enter.text()")

            return False
        elif reply and reply.text:
            text = reply.text
        elif reply and reply.caption:
            text = reply.caption
        elif docs := _.get(f"docs-{command.command}"):
            await message.reply(docs, parse_mode="markdown")

            return False
        else:
            await message.reply(
                _.errors.few_args(num=1), parse_mode="Markdown"
            )

            return False

        return {"query": text}
