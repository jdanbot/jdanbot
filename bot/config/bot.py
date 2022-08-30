from .config import settings

import sys

is_pytest_session = "pytest" in sys.modules

from aiogram import Bot, Dispatcher

if is_pytest_session:
    class FakeUser:
        def is_chat_admin(self) -> bool:
            return True

    class FakeBot(Bot):
        async def get_chat_member(self, *args, **kwargs) -> FakeUser:
            return FakeUser()

    bot = FakeBot(token=settings.tokens.bot_token)
else:
    bot = Bot(token=settings.tokens.bot_token)

dp = Dispatcher(bot)
