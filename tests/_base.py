from pathlib import Path
from typing import Callable
from unittest.async_case import IsolatedAsyncioTestCase

from bot import *  # noqa: F403
from bot.config.bot import router
from bot.database import setup_db
from tests.mocks import mock


class Test:
    def __init__(
        self, message: str, *tasks: tuple[str, str]
    ):
        self.message = message
        self.tasks = tasks


class AbcTests(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        await setup_db()

    async def asyncTearDown(self):
        Path("test.db").unlink()

    async def assertMock(self, x: str, y: str):
        self.assertEqualStrip(await self.run_command(x), y)

    async def assertInMock(self, y: str, x: str):
        self.assertIn(y, await self.run_command(x))

    async def run_command(self, x, **args):
        return await mock(
            self.get_handler_by_command(x), x, **args
        )

    def assertEqualStrip(self, x: str, y: str):
        self.assertEqual(x.strip(), y.strip())

    async def assertBulkMock(self, *tasks: tuple[str, str]):
        for task in tasks:
            await self.assertMock(*task)

    def get_handler_by_command(
        self, command: str
    ) -> Callable:
        fixed_cmd = command.removeprefix("/").split(" ")[0]
        handlers = router.message.handlers

        for handler in handlers:
            commands = handler.flags.get("commands", list())

            for command_raw in commands:
                if fixed_cmd in command_raw.commands:
                    return handler.callback

        raise ValueError
