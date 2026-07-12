from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from msgspec import Struct

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

    class FakeBot:
        def __init__(self, *args, **kwargs): ...
        async def get_chat_member(
            self, *args, **kwargs
        ) -> FakeUser:
            return FakeUser()

    # bot = FakeBot(**bot_params)

    def BotMock(*args, **kwargs): ...

    bot = BotMock

dp: Dispatcher = Dispatcher()
router: Router = Router()


class Commands(Struct):
    __commands: set[tuple[str]] = set()

    def parse_commands_from_router(self, router: Router):
        handlers = router.message.handlers
        for handler in handlers:
            commands = handler.flags.get("commands", list())

            for command_raw in commands:
                self.__commands.add(
                    tuple(command_raw.commands)
                )

    @property
    def listed(self) -> set[tuple[str]]:
        return self.__commands


COMMANDS = Commands()
