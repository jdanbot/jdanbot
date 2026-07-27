from msgspec import Struct, toml

with open("pyproject.toml", "r") as f:

    class PyProject(Struct, frozen=True):
        class Project(Struct, frozen=True):
            version: str

        project: Project

    pyproject = toml.decode(f.read(), type=PyProject)


__version__ = pyproject.project.version
__all__ = [__version__]
