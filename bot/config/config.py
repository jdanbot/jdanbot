import os
import sys
from pathlib import Path

from msgspec import Struct, toml

from .languages import WIKIPEDIA_LANGS

is_test_session = any(
    [
        "pytest" in sys.argv[0],
        "unittest" in sys.argv[0],
    ]
)


class Settings(Struct):
    status: str = "unknown"
    logging_chat: int | None = int(
        os.environ.get("logging_chat", 0)
    )

    db_path: str = os.environ.get("db_path", "jdanbot.db")
    music_path: Path = Path("media/music")

    admin_notes: list[str] = []

    bot_owners_raw: str = os.environ.get(
        "bot_owners_raw", "0"
    )

    class Egg(Struct):
        commands: list[str]
        audio: str

    class Tokens(Struct, frozen=True):
        bot_token: str = ""

    bot_token: str = os.environ.get("bot_token", "")

    tokens: Tokens = Tokens()
    eggs: list[Egg] = []

    @property
    def bot_owners(self) -> list[int]:
        return list(
            map(int, self.bot_owners_raw.split(" "))
        )

    @property
    def token(self) -> str:
        if (
            _ := (self.bot_token or self.tokens.bot_token)
        ) == "":
            raise AttributeError(
                "SET BOT_TOKEN IN ENV OR CONFIG FILE"
            )

        return _


try:
    secret_conf = Path(".secrets.toml").read_text()
except FileNotFoundError:
    secret_conf = ""

settings = toml.decode(
    "\n".join(
        [
            Path("settings.toml").read_text(),
            secret_conf,
        ]
    ),
    type=Settings,
)

if is_test_session:
    settings.db_path = "test.db"

BASE_DIR = Path(__file__).parent.parent.parent
LOCALES_DIR = BASE_DIR / "locales"

WIKIPEDIA_SHORTCUTS = {
    "ru": ["w"],
    "en": ["v"],
    "uk": ["wua", "wikiua", "pawuk"],
    "be-tarask": [
        "wikibe-tarask",
        "wikibet",
        "wbet",
        "xbet",
    ],
}

WIKI_COMMANDS = []

for lang in WIKIPEDIA_LANGS:
    WIKI_COMMANDS.extend([f"wiki{lang}", f"w{lang}"])

for lang in WIKIPEDIA_SHORTCUTS:
    WIKI_COMMANDS.extend(WIKIPEDIA_SHORTCUTS[lang])
