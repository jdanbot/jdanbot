import sys

sys.path.insert(0, ".")

from bot.config.database import Note


Note.delete().execute()


class TestNote:
    def test_get(self):
        assert Note.get(0, "test") is None

    def test_add(self):
        text = "test message"

        Note.add(0, "test", text)
        assert Note.get(0, "test") == text

    def test_show(self):
        assert Note.show(0) == ["test"]

    def test_remove(self):
        Note.remove(0, "test")
        assert Note.get(0, "test") is None
