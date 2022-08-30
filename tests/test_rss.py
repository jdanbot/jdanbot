import sys
import json

sys.path.insert(0, ".")

from bot.config.database import Feed
from bot.timer import save_post

import pytest


params = ["", "test", None]
Feed.delete().execute()


class TestRSS:
    @pytest.mark.asyncio
    async def test_first_save_post(self):
        assert await save_post(*params, "test1") is None
        assert json.loads(list(Feed)[0].links) == ["test1"]

    @pytest.mark.asyncio
    async def test_duplicate_save_post(self):
        assert not await save_post(*params, "test1")
        assert json.loads(list(Feed)[0].links) == ["test1"]

    @pytest.mark.asyncio
    async def test_save_post_with_pin(self):
        assert await save_post(*params, "test2") is None
        assert json.loads(list(Feed)[0].links) == ["test1", "test2"]
