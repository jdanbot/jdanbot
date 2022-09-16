import logging
import traceback

from os import listdir, walk
from pathlib import Path


__version__ = "test"


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
            trace = traceback.format_exc()

            logging.error("{module}: {error}".format(
                module=module,
                error=str(trace).split("\n")[-2]
            ))

            print(trace)


def prepare_paths(
    modules,
    is_folders=False,
    folder_name=None,
    prefix=Path("bot")
):
    if is_folders:
        allowed_folders = filter(lambda x: x not in (
            "__pycache__", "config"), modules)

        return tuple(map(
            lambda folder: prepare_paths(listdir(prefix/folder), folder_name=folder),
            allowed_folders
        ))

    else:
        allowed_modules = filter(
            lambda file: not file.startswith("__") and file.endswith(".py") and
            file[:-3] not in ("ban",),
            modules
        )

        return tuple(map(lambda x: str(prefix/folder_name/x[:-3] if folder_name
                                       else prefix/x[:-3]).replace("/", "."),
                         allowed_modules))


force_import(*prepare_paths(files))
force_import(*prepare_paths(folders, is_folders=True))
# from bot.chat_misc.settings import settings_
force_import("bot.triggers.ban")
