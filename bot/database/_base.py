
import aiosql
from msgspec import Struct


class Base(
    Struct,
    array_like=True,
    frozen=True,
): ...

queries = aiosql.from_path("queries/", "aiosqlite")
