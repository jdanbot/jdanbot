from .config import settings

from aiogram import Bot, Dispatcher
import sys

is_pytest_session = "pytest" in sys.modules


if is_pytest_session:

    class FakeUser:
        status: str = "fake"

        def is_chat_admin(self) -> bool:
            return True

    class FakeBot(Bot):
        async def get_chat_member(self, *args, **kwargs) -> FakeUser:
            return FakeUser()

    bot = FakeBot(token=settings.token)
else:
    bot = Bot(token=settings.token)

dp = Dispatcher(bot)
