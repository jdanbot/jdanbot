from typing import Any

from iso639 import Lang
from msgspec import Struct, convert


class ValidatedStruct(Struct, frozen=True):
    def __post_init__(self, **kwargs):
        convert(kwargs, type=self.__class__)


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


class TranslationLanguage(Struct):
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


class Language(Struct, frozen=True):
    name: str

    alpha_2: str
    alpha_3: str

    @property
    def code(self) -> str:
        return self.alpha_2 or self.alpha_3

    @property
    def google(self) -> str:
        return GOOGLE_LANGS_FIXES.get(self.code, self.code)

    @classmethod
    def from_str(cls, lang: str) -> "Language":
        lang = reverse(GOOGLE_LANGS_FIXES).get(lang, lang)

        if lang == "ua":
            lang = "uk"

        if lang in ["zt", "c"]:
            return convert(
                dict(
                    name=f"SpecialLang {lang}",
                    alpha_2=lang,
                    alpha_3="",
                ),
                Language,
            )

        iso = Language._get(lang)

        return convert(
            dict(
                name=iso.name,
                alpha_2=iso.pt1,
                alpha_3=iso.pt2b or iso.pt3,
            ),
            Language,
        )

    @staticmethod
    def _get(lang: str) -> Lang:
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

GOOGLE_LANGUAGES_TO_CODES = {
    "afrikaans": "af",
    "albanian": "sq",
    "amharic": "am",
    "arabic": "ar",
    "armenian": "hy",
    "assamese": "as",
    "aymara": "ay",
    "azerbaijani": "az",
    "bambara": "bm",
    "basque": "eu",
    "belarusian": "be",
    "bengali": "bn",
    "bhojpuri": "bho",
    "bosnian": "bs",
    "bulgarian": "bg",
    "catalan": "ca",
    "cebuano": "ceb",
    "chichewa": "ny",
    "chinese (simplified)": "zh-CN",
    "chinese (traditional)": "zh-TW",
    "corsican": "co",
    "croatian": "hr",
    "czech": "cs",
    "danish": "da",
    "dhivehi": "dv",
    "dogri": "doi",
    "dutch": "nl",
    "english": "en",
    "esperanto": "eo",
    "estonian": "et",
    "ewe": "ee",
    "filipino": "tl",
    "finnish": "fi",
    "french": "fr",
    "frisian": "fy",
    "galician": "gl",
    "georgian": "ka",
    "german": "de",
    "greek": "el",
    "guarani": "gn",
    "gujarati": "gu",
    "haitian creole": "ht",
    "hausa": "ha",
    "hawaiian": "haw",
    "hebrew": "iw",
    "hindi": "hi",
    "hmong": "hmn",
    "hungarian": "hu",
    "icelandic": "is",
    "igbo": "ig",
    "ilocano": "ilo",
    "indonesian": "id",
    "irish": "ga",
    "italian": "it",
    "japanese": "ja",
    "javanese": "jw",
    "kannada": "kn",
    "kazakh": "kk",
    "khmer": "km",
    "kinyarwanda": "rw",
    "konkani": "gom",
    "korean": "ko",
    "krio": "kri",
    "kurdish (kurmanji)": "ku",
    "kurdish (sorani)": "ckb",
    "kyrgyz": "ky",
    "lao": "lo",
    "latin": "la",
    "latvian": "lv",
    "lingala": "ln",
    "lithuanian": "lt",
    "luganda": "lg",
    "luxembourgish": "lb",
    "macedonian": "mk",
    "maithili": "mai",
    "malagasy": "mg",
    "malay": "ms",
    "malayalam": "ml",
    "maltese": "mt",
    "maori": "mi",
    "marathi": "mr",
    "meiteilon (manipuri)": "mni-Mtei",
    "mizo": "lus",
    "mongolian": "mn",
    "myanmar": "my",
    "nepali": "ne",
    "norwegian": "no",
    "odia (oriya)": "or",
    "oromo": "om",
    "pashto": "ps",
    "persian": "fa",
    "polish": "pl",
    "portuguese": "pt",
    "punjabi": "pa",
    "quechua": "qu",
    "romanian": "ro",
    "russian": "ru",
    "samoan": "sm",
    "sanskrit": "sa",
    "scots gaelic": "gd",
    "sepedi": "nso",
    "serbian": "sr",
    "sesotho": "st",
    "shona": "sn",
    "sindhi": "sd",
    "sinhala": "si",
    "slovak": "sk",
    "slovenian": "sl",
    "somali": "so",
    "spanish": "es",
    "sundanese": "su",
    "swahili": "sw",
    "swedish": "sv",
    "tajik": "tg",
    "tamil": "ta",
    "tatar": "tt",
    "telugu": "te",
    "thai": "th",
    "tigrinya": "ti",
    "tsonga": "ts",
    "turkish": "tr",
    "turkmen": "tk",
    "twi": "ak",
    "ukrainian": "uk",
    "urdu": "ur",
    "uyghur": "ug",
    "uzbek": "uz",
    "vietnamese": "vi",
    "welsh": "cy",
    "xhosa": "xh",
    "yiddish": "yi",
    "yoruba": "yo",
    "zulu": "zu",
}

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

GLANGS = [
    Language.from_str(lang) for lang in GTRANSLATE_LANGS
]
