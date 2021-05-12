import os

import yaml
import i18n

from aiogram.contrib.middlewares.i18n import I18nMiddleware as I18nMiddlewareBase


class I18nMiddleware(I18nMiddlewareBase):
    def t(self, singular, plural=None, n=1, locale=None, **kwargs):
        self.i18n = i18n
        self.i18n.load_path.append(self.path)

        res = self.gettext(singular, plural, n, locale)
        lang = self.ctx_locale.get()

        self.i18n.set("locale", lang)
        self.i18n.set("fallback", self.default)

        try:
            return self.i18n.t(res, **kwargs)
        except TypeError:
            with open(f"{self.path}/{res.split('.')[0]}.{lang}.yml",
                      encoding="UTF-8") as f:
                locale = yaml.safe_load(f.read())
                translate = locale.get(lang).get(res.split(".")[1])
                return [_.format(**kwargs) for _ in translate]
