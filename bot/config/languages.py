from dataclasses import dataclass


@dataclass
class Language:
    emoji: str
    name: str


LANGS = {
    "ru": Language("🇷🇺", "Русский"),
    "en": Language("🇬🇧", "English"),
    "uk": Language("🇺🇦", "Українська"),
    "be": Language("🇧🇾", "Беларуская"),
    "pl": Language("🇵🇱", "Polski"),
    "it": Language("🇮🇹", "Italiano"),
    "la": Language("🇻🇦", "Lingua Latina"),
    "de": Language("🇩🇪", "Deutsch"),
    "fr": Language("🇫🇷", "Français"),
    "kz": Language("🇰🇿", "Қазақша"),
    "hu": Language("🇭🇺", "Magyar"),
    "hi": Language("🇮🇳", "हिन्दी"),
    "he": Language("🇮🇱", "עִבְרִית"),
    "hr": Language("🇭🇷", "Hrvatski"),
    "ja": Language("🇯🇵", "日本語"),
    "cs": Language("🇨🇿", "Czech čeština"),
    "no": Language("🇳🇴", "Norsk"),
    "pt": Language("🇵🇹", "Português"),
    -1: Language("🏳️", "NoneLanguage"),
}

GTRANSLATE_LANGS = {
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
