from .lib.middleware import I18nMiddleware, SpyMiddleware

from .config import LOCALES_DIR
from .bot import dp

i18n = I18nMiddleware("bot", LOCALES_DIR, default="ru")
dp.middleware.setup(i18n)
dp.middleware.setup(SpyMiddleware())

_ = i18n.t
