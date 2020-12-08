from os import listdir

files = listdir("bot")
__all__ = []

for file in files:
    if file.endswith(".py") \
       and not file.startswith("__") \
       and not file == "bot.py":
        __all__.append(file[:-3])
