from .token import heroku
from os import listdir

files = listdir("bot/components") if heroku else listdir("components")
__all__ = []

for file in files:
    if file.endswith(".py") and not file == "__init__.py":
        __all__.append(file[:-3])
