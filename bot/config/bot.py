import sys

from aiogram import Dispatcher
from .config import TOKEN

if "pytest" in sys.modules:
    from .lib.fake_bot import FakeBot, FakeDispatcher

    bot = FakeBot()
    dp = FakeDispatcher(bot)

else:
    from aiogram import Bot

    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot)

