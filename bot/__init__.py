from os import listdir, walk

files = None
folders = None

for _, dirs, files in walk("bot", topdown=True):
    files = files
    folders = dirs
    break

__all__ = []

for folder in folders:
    if folder != "lib" and folder != "__pycache__" and folder != "cache":
        for file in listdir(f"bot/{folder}"):
            if file != "__pycache__" and file.endswith(".py"):
                __import__(f"bot.{folder}.{file[:-3]}")

for file in files:
    if file.endswith(".py") \
       and not file.startswith("__"):
        __all__.append(file[:-3])