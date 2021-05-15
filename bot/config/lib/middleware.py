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

        lang = self.default if lang is None else lang
        lang = "uk" if lang == "ua" else lang

        self.i18n.set("locale", lang)
        self.i18n.set("fallback", self.default)

        try:
            return self.i18n.t(res, **kwargs)
        except TypeError:
            path = f"{self.path}/{res.split('.')[0]}.{{lang}}.yml"

            if not os.path.exists(path.format(lang=lang)):
                lang = self.default

            with open(path.format(lang=lang),
                      encoding="UTF-8") as f:
                locale = yaml.safe_load(f.read())
                translate = locale.get(lang).get(res.split(".")[1])

                print(translate)
                return [_.format(**kwargs) if isinstance(_, str) else _
                        for _ in translate]
