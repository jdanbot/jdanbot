from .lib.middleware import I18nMiddleware, SpyMiddleware

from pyi18n_new import I18N

from .config import LOCALES_DIR
from .bot import dp

i18n = I18nMiddleware("bot", LOCALES_DIR, default="en")
i18n.pyi18n: I18N = I18N(LOCALES_DIR, default="en", fallback="ru")

dp.middleware.setup(i18n)
dp.middleware.setup(SpyMiddleware())

_ = i18n.t
