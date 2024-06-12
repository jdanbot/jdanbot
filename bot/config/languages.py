from dataclasses import dataclass
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES
from typing import Any

from pydantic import BaseModel

from iso639 import Lang

GOOGLE_LANGS_FIXES = {
    "he": "iw",
    "jv": "jw",
    "zh": "zh-CN",
    "zt": "zh-TW",
    "mni": "mni-Mtei",
    "c": "_crazy",
}


def reverse(d: dict[str, str]) -> dict[str, str]:
    return {value: key for key, value in d.items()}


@dataclass
class TranslationLanguage:
    emoji: str
    name: str


def get_key_by_value(x: dict[Any, Any], value: Any) -> str:
    return list(x.keys())[list(x.values()).index(value)]


LANGS = {
    "ru": TranslationLanguage("🇷🇺", "Русский"),
    "en": TranslationLanguage("🇬🇧", "English"),
    "uk": TranslationLanguage("🇺🇦", "Українська"),
    "be": TranslationLanguage("🇧🇾", "Беларуская"),
    "pl": TranslationLanguage("🇵🇱", "Polski"),
    "it": TranslationLanguage("🇮🇹", "Italiano"),
    "la": TranslationLanguage("🇻🇦", "Lingua Latina"),
    "de": TranslationLanguage("🇩🇪", "Deutsch"),
    -1: TranslationLanguage("🏳️", "NoneLanguage"),
}


class Language(BaseModel):
    name: str

    alpha_2: str
    alpha_3: str

    @property
    def code(self) -> str:
        return self.alpha_2 or self.alpha_3

    @property
    def google(self) -> str:
        return GOOGLE_LANGS_FIXES.get(self.code, self.code)

    def __init__(self, lang: str) -> "Language":  # type: ignore
        lang = reverse(GOOGLE_LANGS_FIXES).get(lang, lang)

        if lang == "ua":
            lang = "uk"

        if lang in ["zt", "c"]:
            super(Language, self).__init__(
                name=f"SpecialLang {lang}",
                alpha_2=lang,
                alpha_3="",
            )

            return None  # type: ignore

        l = self._get(lang)

        super(Language, self).__init__(
            name=l.name,  # type: ignore
            alpha_2=l.pt1,  # type: ignore
            alpha_3=l.pt2b or l.pt3,  # type: ignore
        )

    @staticmethod
    def _get(lang: str) -> tuple:
        try:
            return Lang(lang)
        except Exception as e:
            try:
                return Lang(
                    get_key_by_value(
                        GOOGLE_LANGUAGES_TO_CODES, lang
                    ).title()
                )
            except Exception:
                raise e


GTRANSLATE_LANGS = list(
    {
        *GOOGLE_LANGUAGES_TO_CODES.values(),
        "he",
        "jv",
        "zh",
        "zt",
        "mni",
        "ua",
    }
)

GLANGS = [Language(lang) for lang in GTRANSLATE_LANGS]

CRAZY_LANGS = {
    "ru",
    "en",
    "ua",
    "uk",
    "be",
    "pl",
    "de",
    "fr",
    "kz",
    "hu",
    "hi",
    "he",
    "hr",
    "ja",
    "cs",
    "no",
    "pt",
    "tt",
}

WIKIPEDIA_LANGS = [
    "ru",
    "en",
    "sv",
    "de",
    "ce",
    "tt",
    "ba",
    "pl",
    "uk",
    "be",
    "es",
    "he",
    "xh",
    "ab",
    "it",
    "fr",
    "la",
    "be-tarask",
]
