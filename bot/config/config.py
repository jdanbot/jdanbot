from pydantic import BaseModel
from pydantic_settings import BaseSettings

from pathlib import Path

from .languages import WIKIPEDIA_LANGS

import toml


class Settings(BaseSettings):
    status: str = "unknown"
    logging_chat: int = None

    db_path: Path = Path("jdanbot.db")
    music_path: Path = Path("media/music")

    admin_notes: list[str]

    bot_owners_raw: str = "0"

    api_url: str = "http://127.0.0.1:8000"

    class Schedule(BaseModel):
        delay_seconds: int = 20

        katz_bots: bool = False

    class Egg(BaseModel):
        commands: list[str]
        audio: Path

    class Tokens(BaseModel):
        bot_token: str = ""

    bot_token: str = ""

    tokens: Tokens = Tokens()
    schedule: Schedule = Schedule()
    eggs: list[Egg]

    @property
    def bot_owners(self) -> list[int]:
        return list(map(int, self.bot_owners_raw.split(" ")))

    @property
    def token(self) -> str:
        if (_ := self.bot_token or self.tokens.bot_token) == "":
            raise AttributeError(
                "SET BOT_TOKEN IN ENV OR CONFIG FILE"
            )

        return _


try:
    with open("settings.toml") as file:
        settings_file = toml.loads(file.read())

    with open(".secrets.toml") as file:
        secrets_file = toml.loads(file.read())

    settings = Settings.model_validate(settings_file | secrets_file)
except Exception:
    settings = Settings.model_validate(settings_file)


BASE_DIR = Path(__file__).parent.parent.parent
LOCALES_DIR = BASE_DIR / "locales"

WIKIPEDIA_SHORTCUTS = {
    "ru": ["w"],
    "en": ["v"],
    "uk": ["wua", "wikiua", "pawuk"],
    "be-tarask": ["wikibe-tarask", "wikibet", "wbet", "xbet"],
}

WIKI_COMMANDS = []

for lang in WIKIPEDIA_LANGS:
    WIKI_COMMANDS.extend([f"wiki{lang}", f"w{lang}"])

for lang in WIKIPEDIA_SHORTCUTS:
    WIKI_COMMANDS.extend(WIKIPEDIA_SHORTCUTS[lang])
