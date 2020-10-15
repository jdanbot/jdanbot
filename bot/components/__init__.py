from os import listdir

__all__ = []

for file in listdir("components"):
    if file.endswith(".py") and not file == "__init__.py":
        __all__.append(file[:-3])
