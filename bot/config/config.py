import yaml

from pathlib import Path
from os import environ


class Config:
    def __init__(self, file_path="config.yml"):
        try:
            with open(file_path, encoding="UTF-8") as file:
                self.config = yaml.full_load(file.read())
        except Exception:
            self.config = {}

        self.environ = environ

    def get(self, param, default=None):
        globals()[param.upper()] = (
            self.environ.get(param.upper()) or
            self.config.get(param, default))


config = Config()
config.get("db_path", default="jdanbot.db")
config.get("delay", default=30)
config.get("rss_feeds", default=[])
config.get("rss", default=False)
config.get("image_path", default="bot/cache/{image}.jpg")
config.get("token")
config.get("status", default="unknown")
config.get("vk", default=False)
config.get("vk_channels", default=())
config.get("access_token", default="")
config.get("katz_bots", default=False)
config.get("youtube", default=False)
config.get("youtube_channels", default=())
config.get("youtube_key", default=None)
config.get("langs_list", default=[
    "ru", "en", "sv", "de", "ce",
    "tt", "ba", "pl", "uk", "be",
    "es", "he", "xh", "ab"])

config.get("unique_commands", default={
    "ru": ["wikiru2", "w", "wiki"],
    "en": ["van", "wen", "v"],
    "uk": ["wikiua", "wua", "pawuk"],
    "be-tarask": ["wikibe-tarask", "wikibet", "wbet", "xbet"]
})

config.get("admin_notes", default=[
    "__rules__",
    "__enable_bot__",
    "__ban__",
    "__welcome__",
    "__enable_response__",
    "__enable_welcome__",
    "__enable_greatings__",
    "__warns_to_ban__"
])

config.get("eggs", default=[
    {"commands": ["java1"], "audio": "java.ogg"},
    {"commands": ["cool_music"], "audio": "music.ogg"},
    {"commands": ["cum"], "audio": "cum.ogg"},
    {"commands": ["longcum"], "audio": "longcum.ogg"},
    {"commands": ["frog"], "audio": "lyagushka.ogg"}])

config.get("stickers", {
    "pizda": "CAACAgIAAx0CUDyGjwACAQxfCFkaHE52VvWZzaEDQwUC8FYa-wAC3wADlJlpL5sCLYkiJrDFGgQ",
    "net_pizdy": "CAACAgIAAx0CUDyGjwACAQ1fCFkcDHIDN_h0qHDu7LgvS8SBIgAC4AADlJlpL8ZF00AlPORXGgQ",
    "pizda_tebe": "CAACAgIAAxkBAAILHV9qcv047Lzwp_B64lDlhtOD-2RGAAIgAgAClJlpL5VCBwPTI85YGwQ",
    "xui": "CAACAgIAAx0CUDyGjwACAQ5fCFkeR-pVhI_PUTcTbDGUOgzwfAAC4QADlJlpL9ZRhbtO0tQzGgQ",
    "net_xua": "CAACAgIAAx0CUDyGjwACAQ9fCFkfgfI9pH9Hr96q7dH0biVjEwAC4gADlJlpL_foG56vPzRPGgQ"
})

BASE_DIR = Path(__file__).parent.parent
LOCALES_DIR = BASE_DIR / "i18n"
