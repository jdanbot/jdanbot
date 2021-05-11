from aiogram import Bot, Dispatcher, executor, types
from .lib.middleware import I18nMiddleware

from .config import TOKEN, LOCALES_DIR

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

i18n = I18nMiddleware("bot", LOCALES_DIR)
dp.middleware.setup(i18n)

_ = i18n.t
