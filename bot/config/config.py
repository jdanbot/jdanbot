import yaml

from pathlib import Path
from os import environ


class Config:
    def __init__(self, config_path="config.yml", **kwargs):
        try:
            with open(config_path, encoding="UTF-8") as file:
                self.config = yaml.full_load(file.read())
        except Exception:
            self.config = {}

        self.environ = environ

        for param in kwargs:
            value = self.get(param, default=kwargs[param])

    def get(self, param, default=None):
        globals()[param.upper()] = (
            self.environ.get(param.upper()) or
            self.config.get(param, default))


Config(
    db_path="jdanbot.db",
    delay=30,
    rss_feeds=(),
    rss=False,
    image_path="bot/cache/{image}.jpg",
    status="unknown",
    vk=False,
    vk_channels=(),
    access_token="",
    katz_bots=False,
    youtube=False,
    youtube_channels=(),
    youtube_key="",
    langs_list=[
        "ru", "en", "sv", "de", "ce",
        "tt", "ba", "pl", "uk", "be",
        "es", "he", "xh", "ab"],

    unique_commands={
        "ru": ["wikiru2", "w", "wiki"],
        "en": ["van", "wen", "v"],
        "uk": ["wikiua", "wua", "pawuk"],
        "be-tarask": ["wikibe-tarask", "wikibet", "wbet", "xbet"]},

    admin_notes=[
        "__rules__",
        "__enable_bot__",
        "__ban__",
        "__welcome__",
        "__enable_response__",
        "__enable_welcome__",
        "__enable_greatings__",
        "__warns_to_ban__",
        "__chat_lang__",
        "__enable_admin__"],

    eggs=[
        {"commands": ["java1"], "audio": "java.ogg"},
        {"commands": ["cool_music"], "audio": "music.ogg"},
        {"commands": ["cum"], "audio": "cum.ogg"},
        {"commands": ["longcum"], "audio": "longcum.ogg"},
        {"commands": ["frog"], "audio": "lyagushka.ogg"}],

    stickers={
        "pizda": "CAACAgIAAx0CUDyGjwACAQxfCFkaHE52VvWZzaEDQwUC8FYa-wAC3wADlJlpL5sCLYkiJrDFGgQ",
        "net_pizdy": "CAACAgIAAx0CUDyGjwACAQ1fCFkcDHIDN_h0qHDu7LgvS8SBIgAC4AADlJlpL8ZF00AlPORXGgQ",
        "pizda_tebe": "CAACAgIAAxkBAAILHV9qcv047Lzwp_B64lDlhtOD-2RGAAIgAgAClJlpL5VCBwPTI85YGwQ",
        "xui": "CAACAgIAAx0CUDyGjwACAQ5fCFkeR-pVhI_PUTcTbDGUOgzwfAAC4QADlJlpL9ZRhbtO0tQzGgQ",
        "net_xua": "CAACAgIAAx0CUDyGjwACAQ9fCFkfgfI9pH9Hr96q7dH0biVjEwAC4gADlJlpL_foG56vPzRPGgQ"},

    token=None,
    gtranslate_langs=["ru", "en", "uk", "be", "pl", "de"]
)

BASE_DIR = Path(__file__).parent.parent
LOCALES_DIR = BASE_DIR / "i18n"


MAX_URL = "https://img.youtube.com/vi/{id}/maxresdefault.jpg"
HQ_URL = "https://img.youtube.com/vi/{id}/hqdefault.jpg"
