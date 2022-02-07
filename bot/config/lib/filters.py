import asyncio
import logging

from .text import code
from ..bot import bot


class ResendLogs(logging.Filter):
    def filter(self, record) -> bool:
        loop = asyncio.get_event_loop()
        loop.create_task(self.send_to_tg(record))
        return True

    async def send_to_tg(self, record):
        await bot.send_message(-1001435542296, code(record.msg),
                               parse_mode="HTML")


class NoRunningJobFilter(logging.Filter):
    def filter(self, record):
        return not record.getMessage().startswith("Running job Every")
