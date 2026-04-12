import sys

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from .config import settings

is_pytest_session = any("pytest" in arg for arg in sys.argv)

bot_params = dict(
    token=settings.token,
    default=DefaultBotProperties(
        parse_mode=ParseMode.MARKDOWN_V2
    ),
)


if is_pytest_session:

    class FakeUser:
        status: str = "fake"

        def is_chat_admin(self) -> bool:
            return True

    class FakeBot(Bot):
        async def get_chat_member(
            self, *args, **kwargs
        ) -> FakeUser:
            return FakeUser()

    bot = FakeBot(**bot_params)
else:
    bot = Bot(**bot_params)

dp: Dispatcher = Dispatcher()
router: Router = Router()
