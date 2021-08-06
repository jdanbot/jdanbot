import sys
import asyncio

sys.path.insert(0, ".")

from bot.config.database import manager, Note

import pytest


asyncio.run(manager.execute(
    Note.delete()
))


class TestNote:
    @pytest.mark.asyncio
    async def test_get(self):
        assert await Note.get(0, "test") is None

    @pytest.mark.asyncio
    async def test_add(self):
        text = "test message"

        await Note.add(0, "test", text)
        assert await Note.get(0, "test") == text

    @pytest.mark.asyncio
    async def test_show(self):
        assert await Note.show(0) == ["test"]

    @pytest.mark.asyncio
    async def test_remove(self):
        await Note.remove(0, "test")
        assert await Note.get(0, "test") is None