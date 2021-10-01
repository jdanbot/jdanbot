import sys

sys.path.insert(0, ".")

from bot.config.database import Video
from bot.timer import save_post

import pytest


params = ["", "test", None]
Video.delete().execute()


class TestRSS:
    @pytest.mark.asyncio
    async def test_first_save_post(self):
        assert await save_post(*params, "test1") is None

    @pytest.mark.asyncio
    async def test_duplicate_save_post(self):
        assert not await save_post(*params, "test1")

    @pytest.mark.asyncio
    async def test_save_post_with_pin(self):
        assert await save_post(*params, "test2") is None
