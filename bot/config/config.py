from pydantic import BaseSettings, BaseModel

from pathlib import Path

from .languages import WIKIPEDIA_LANGS

import toml


class Settings(BaseSettings):
    status: str = "unknown"
    logging_chat: int = None

    db_path: Path = Path("jdanbot.db")
    music_path: Path = Path("media/music")

    admin_notes: list[str]

    class Tokens(BaseModel):
        bot_token: str

    class Schedule(BaseModel):
        delay_seconds: int = 20

        katz_bots: bool = False

    class Egg(BaseModel):
        commands: list[str]
        audio: Path

    tokens: Tokens
    schedule: Schedule = Schedule()
    eggs: list[Egg]


with open("settings.toml") as file:
    settings_file = toml.loads(file.read())

with open(".secrets.toml") as file:
    secrets_file = toml.loads(file.read())

settings = Settings.parse_obj(settings_file | secrets_file)

BASE_DIR = Path(__file__).parent.parent.parent
LOCALES_DIR = BASE_DIR / "locales"

WIKIPEDIA_SHORTCUTS = {
    "ru": ["w"],
    "en": ["v"],
}

WIKI_COMMANDS = []

for lang in WIKIPEDIA_LANGS:
    WIKI_COMMANDS.extend([f"wiki{lang}", f"w{lang}"])

for lang in WIKIPEDIA_SHORTCUTS:
    WIKI_COMMANDS.extend(WIKIPEDIA_SHORTCUTS[lang])
