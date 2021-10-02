import sys

sys.path.insert(0, ".")

from bot.config.database import Event
from bot.config.lib.fake_bot import FakeMessage


Event.delete().execute()


class TestEvent:
    def test_reg_user_in_db(self):
        message = FakeMessage()
        assert Event.reg_user_in_db(message)

    def test_check_user_in_db(self):
        message = FakeMessage()
        print(Event.reg_user_in_db(message))
        assert Event.reg_user_in_db(message) is None
