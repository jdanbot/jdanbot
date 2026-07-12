from aiogram.utils.markdown import code
from art import text2art

from bot.config.lib.locales import locales

from ._base import AbcTests

_ = locales.ru


class Tests(AbcTests):
    async def test_mocks(self):
        await self.assertMock("/bylo", "Было")

    async def test_pidor_first_run(self):
        await self.assertBulkMock(
            ("/pidor", _.pidor.reg),
            ("/pidorreg", _.pidor.in_db),
            ("/pidorreg", _.pidor.already_in_db),
            # ("/pidor", "@test"),
        )

    async def test_notes_simple(self):
        NOTE = "abc"

        await self.assertBulkMock(
            (f"/get {NOTE}", _.notes.create_var(name=NOTE)),
            (f"/remove {NOTE}", _.notes.not_found),
            (f"/set {NOTE} 42", _.notes.add_note),
            (f"/get {NOTE}", "42"),
            ("/show", "abc"),
            (f"/remove {NOTE}", _.notes.successful_deleted),
            ("/show", _.notes.no_notes),
            (f"/get {NOTE}", _.notes.create_var(name=NOTE)),
        )

    async def test_misc(self):
        await self.assertBulkMock(
            # ("/mute 5 test", ""),
            (
                "/art test",
                code(text2art("test", chr_ignore=True)),
            ),
            ("/calc 5+5", "`10`"),
            # ("/eval 2*2+2", "`6`"),
            ("/tru test", "тест"),
        )
