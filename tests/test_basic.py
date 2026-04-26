from pathlib import Path
from unittest.async_case import IsolatedAsyncioTestCase

from bot.chat_misc.pidor import find_pidor, reg_pidor
from bot.config.lib.locales import locales
from bot.database import setup_db
from bot.memes.memes import bylo
from tests.mocks import mock

_ = locales.ru


class Tests(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        await setup_db()

    async def asyncTearDown(self):
        Path("test.db").unlink()
        ...

    def test_basis(self):
        self.assertTrue(True)

    async def test_mocks(self):
        self.assertEqual(
            await mock(bylo, "/bylo"),
            "Было",
        )

    async def test_pidor_first_run(self):
        self.assertEqual(
            await mock(find_pidor, "/pidor"),
            _.pidor.reg,
        )
        self.assertEqual(
            await mock(reg_pidor, "/pidorreg"),
            _.pidor.in_db,
        )
        self.assertEqual(
            await mock(reg_pidor, "/pidorreg"),
            _.pidor.already_in_db,
        )
