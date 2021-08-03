import sys

sys.path.insert(0, ".")

from pathlib import Path

from bot.config.lib.middleware import I18nMiddleware
from bot.lib.text import prettyword


BASE_DIR = Path(__file__).parent.parent
LOCALES_DIR = BASE_DIR / "locales"

i18n = I18nMiddleware("bot", LOCALES_DIR, default="ru")
_ = i18n.t


class TestLocaleMiddleware:
    def test_locale(self):
        text = "Админ не может отменить пред сам себе"
        assert _("ban.admin_cant_unwarn_self") == text

    def test_locale_count(self):
        text = "Ты никогда не был пидором дня"
        assert _("pidor.me", count=0) == text

    def test_locale_fcount(self):
        text = "А ты опытный пидор... Видел тебя 100 раз"

        #REWRITE: Integrate prettyword to i18n middleware or use normal p-i18n
        assert _("pidor.me", count=100,
                 fcount=prettyword(100, _("cases.count"))) == text

    def test_locale_with_args(self):
        text = "*Пожалуйста, напишите название статьи*\nНапример так: `/w Название Статьи`"
        assert _("errors.enter_wiki_query").format("/w") == text

    def test_locale_ban(self):
        assert _("triggers.ban_messages")[795449748]