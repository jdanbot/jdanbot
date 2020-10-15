from .token import heroku
from os import listdir

files = listdir("bot/components") if heroku else listdir("components")
__all__ = []

print(f"{files = }")

for file in files:
    if file.endswith(".py") and not file == "__init__.py":
        print(f"{file = }")
        __all__.append(file[:-3])
