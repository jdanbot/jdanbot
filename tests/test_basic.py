from aiogram.utils.markdown import code
from art import text2art

from bot.config.lib.locales import locales

from ._base import AbcTests

_ = locales.ru


YOUTU_BE_LINK = "https://youtu.be/dQw4w9WgXcQ"
ANSWER1 = "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
YOUTUBE_COM_LINK = (
    "https://www.youtube.com/watch?v=r40AvHs3uJE"
)
ANSWER2 = "https://img.youtube.com/vi/r40AvHs3uJE/maxresdefault.jpg"


class Tests(AbcTests):
    async def test_mocks(self):
        await self.assertMock("/bylo", "Было")

    async def test_pidor_first_run(self):
        await self.assertBulkMock(
            ("/pidor", _.pidor.reg),
            ("/pidorreg", _.pidor.in_db),
            ("/pidorreg", _.pidor.already_in_db),
        )

        await self.assertInMock("@johndoe", "/pidor")
        await self.assertInMock("**johndoe**", "/pidor")

    async def test_notes_simple(self):
        NOTE = "abc"

        await self.assertBulkMock(
            (f"/get {NOTE}", _.notes.create_var(name=NOTE)),
            (f"/remove {NOTE}", _.notes.not_found),
            (f"/set {NOTE} 42", _.notes.add_note),
            (f"/get {NOTE}", "42"),
            (f"/set {NOTE} 52", _.notes.edit_note),
            (f"/set else {NOTE}", _.notes.add_note),
            ("/show", f"{NOTE}, else"),
            (f"/remove {NOTE}", _.notes.successful_deleted),
            ("/remove else", _.notes.successful_deleted),
            ("/remove else", _.notes.not_found),
            ("/show", _.notes.no_notes),
            (f"/get {NOTE}", _.notes.create_var(name=NOTE)),
        )

    async def test_misc(self):
        await self.assertBulkMock(
            (
                "/art test",
                code(text2art("test", chr_ignore=True)),
            ),
            ("/calc 5+5", "`10`"),
            # ("/eval 2*2+2", "`6`"),
            ("/tru test", "тест"),
            (f"/preview {YOUTU_BE_LINK}", ANSWER1),
            (f"/preview {YOUTUBE_COM_LINK}", ANSWER2),
        )

    async def test_admin_functions(self):
        await self.assertInMock("1\\-й", "/warn test")
        await self.assertInMock("2\\-й", "/warn test")
        await self.assertInMock("выдал мут", "/warn test")
        await self.assertInMock("выдал мут", "/mute 5 test")
