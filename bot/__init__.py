from os import listdir, walk
from pathlib import Path

try:
    from rich.console import Console
    from rich.traceback import Traceback

    console = Console()
except ModuleNotFoundError:
    import traceback

    console = None


IGNORED_MODULES = {
    "__pycache__",
    "config",
    "database",
    "lib",
}


def force_import(*args):
    for module in args:
        if isinstance(module, tuple):
            force_import(*module)
            continue

        try:
            __import__(module)

        except Exception as e:
            if console:
                console.print(Traceback())
            else:
                traceback.print_exception(e)


def prepare_paths(
    modules,
    folder_name=None,
    prefix=Path("bot"),
):
    allowed_modules = filter(
        lambda file: (
            not file.startswith("_")
            and file.endswith(".py")
            and file[:-3] not in ("ban", "ocr")
        ),
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


def prepare_paths_folders(
    modules,
    folder_name=None,
    prefix=Path("bot"),
):
    allowed_folders = set(modules) - IGNORED_MODULES

    return tuple(
        map(
            lambda folder: prepare_paths(
                listdir(prefix / folder),
                folder_name=folder,
            ),
            allowed_folders,
        )
    )


__import__("bot.config.logger")
__import__("bot.filters")
root, folders, files = walk("bot", topdown=True).__next__()

force_import(*prepare_paths_folders(folders))
force_import("bot.triggers.ban")
force_import("bot.chat_misc.ocr")
