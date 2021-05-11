import os
from aiogram.contrib.middlewares.i18n import I18nMiddleware as I18nMiddlewareBase
import i18n


class I18nMiddleware(I18nMiddlewareBase):
    def t(self, singular, plural=None, n=1, locale=None, **kwargs):
        self.i18n = i18n
        self.i18n.load_path.append(self.path)

        res = self.gettext(singular, plural, n, locale)

        self.i18n.set("locale", self.ctx_locale.get())
        self.i18n.set("fallback", self.default)

        return self.i18n.t(res, **kwargs)
