import sys

from dynaconf import Dynaconf
from pathlib import Path


settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=["default_settings.toml", 'settings.toml', '.secrets.toml'],
)

for key in ("common", "schedule", "rss_feeds",
            "youtube_feeds", "vk_feeds", "tokens",
            "unique_commands", "stickers",
            "links", "eggs"):
    value = settings.get(key, default=None)

    if isinstance(value, dict) \
       and key not in ("unique_commands", "stickers", "eggs"):
        for _ in value:
            globals()[_.upper()] = value[_]

    else:
        globals()[key.upper()] = value


BASE_DIR = Path(__file__).parent.parent.parent
LOCALES_DIR = BASE_DIR / "locales"


if not settings.common.memory_db_patch:
    TEMP_DB_PATH = "file:cachedb?mode=memory&cache=shared"
else:
    TEMP_DB_PATH = "file:memory?cache=shared"

if "pytest" in sys.modules:
    DB_PATH = TEMP_DB_PATH


WIKICOMMANDS = []

for lang in settings.common.langs_list:
    WIKICOMMANDS.extend([f"wiki{lang}", f"w{lang}"])

for lang in settings.unique_commands:
    WIKICOMMANDS.extend(settings.unique_commands[lang])
