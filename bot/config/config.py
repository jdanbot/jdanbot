from pydantic import BaseSettings, BaseModel, AnyHttpUrl, Field

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
        bot_token: str = Field(alias="token")
        youtube_token: str = Field(alias="youtube_key")

    class Schedule(BaseModel):
        delay_seconds: int = 20

        katz_bots: bool = False
        youtube: bool = False

    class RSSFeed(BaseModel):
        chat_id: int
        feed_id: str
        source: AnyHttpUrl = Field(alias="url")

    class YoutubeFeed(BaseModel):
        chat_id: int
        feed_id: str
        # channel_id: str = feed_id

    class Egg(BaseModel):
        commands: list[str]
        audio: Path

    eggs: list[Egg]

    tokens: Tokens

    schedule: Schedule = Schedule()

    rss_feeds: list[RSSFeed] = []
    youtube_feeds: list[YoutubeFeed] = []


with open("settings.toml") as file:
    settings_file = toml.loads(file.read())

with open(".secrets.toml") as file:
    secrets_file = toml.loads(file.read())

settings = Settings.parse_obj(settings_file | secrets_file)

BASE_DIR = Path(__file__).parent.parent.parent
LOCALES_DIR = BASE_DIR / "locales"

UNIQUE_COMMANDS = {
    "ru": ["wikiru2", "w", "wiki"],
    "en": ["van", "wen", "v"],
    "uk": ["wikiua", "wua", "pawuk"],
    "be-tarask": ["wikibe-tarask", "wikibet", "wbet", "xbet"]
}


WIKICOMMANDS = []

for lang in WIKIPEDIA_LANGS:
    WIKICOMMANDS.extend([f"wiki{lang}", f"w{lang}"])

for lang in UNIQUE_COMMANDS:
    WIKICOMMANDS.extend(UNIQUE_COMMANDS[lang])
