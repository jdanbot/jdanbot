import sys
import asyncio

sys.path.insert(0, ".")

from bot.config.database import manager, Event
from bot.config.lib.fake_bot import FakeMessage

import pytest


asyncio.run(manager.execute(
    Event.delete()
))


class TestEvent:
    @pytest.mark.asyncio
    async def test_reg_user_in_db(self):
        message = FakeMessage()
        assert await Event.reg_user_in_db(message)

    @pytest.mark.asyncio
    async def test_check_user_in_db(self):
        message = FakeMessage()
        assert await Event.reg_user_in_db(message) is None