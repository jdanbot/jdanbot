import sys
from os import listdir, walk
from pathlib import Path

from rich.console import Console
from rich.traceback import Traceback

is_pytest_session = "pytest" in sys.modules
console = Console()


__import__("bot.config.logger")
__import__("bot.filters")
root, folders, files = walk("bot", topdown=True).__next__()


def force_import(*args):
    for module in args:
        if isinstance(module, tuple):
            force_import(*module)
            continue

        try:
            __import__(module.replace("\\", "."))

        except Exception:
            console.print(Traceback())


def prepare_paths(
    modules,
    is_folders=False,
    folder_name=None,
    prefix=Path("bot"),
):
    if is_folders:
        allowed_folders = filter(
            lambda x: x not in ("__pycache__", "config"),
            modules,
        )

        return tuple(
            map(
                lambda folder: prepare_paths(
                    listdir(prefix / folder),
                    folder_name=folder,
                ),
                allowed_folders,
            )
        )

    else:
        allowed_modules = filter(
            lambda file: not file.startswith("__")
            and file.endswith(".py")
            and file[:-3] not in ("ban", "ocr"),
            modules,
        )

        return tuple(
            map(
                lambda x: str(
                    prefix / folder_name / x[:-3]
                    if folder_name
                    else prefix / x[:-3]
                ).replace("/", "."),
                allowed_modules,
            )
        )


if not is_pytest_session:
    force_import(*prepare_paths(files))
    force_import(*prepare_paths(folders, is_folders=True))
    from bot.chat_misc.settings import settings_

    force_import("bot.triggers.ban")
    force_import("bot.chat_misc.ocr")
