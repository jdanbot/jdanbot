from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from .config import is_test_session, settings

bot_params = dict(
    token=settings.token,
    default=DefaultBotProperties(
        parse_mode=ParseMode.MARKDOWN_V2
    ),
)


if not is_test_session:
    bot = Bot(**bot_params)
else:

    class FakeUser:
        status: str = "fake"

        def is_chat_admin(self) -> bool:
            return True

    class FakeBot(Bot):
        async def get_chat_member(
            self, *args, **kwargs
        ) -> FakeUser:
            return FakeUser()

    # bot = FakeBot(**bot_params)

    def BotMock(*args, **kwargs): ...

    bot = BotMock

dp: Dispatcher = Dispatcher()
router: Router = Router()
