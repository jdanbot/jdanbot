import sys

sys.path.insert(0, ".")

from bot.config.database import manager, Video
from bot.timer import save_post

import pytest


class TestRSS:
    @pytest.mark.asyncio
    async def test_save_post(self):
        params = ["", "test", None]

        await manager.execute(Video.delete())

        assert await save_post(*params, "test1") is None
        assert not await save_post(*params, "test1")
        assert await save_post(*params, "test2") is None