import sqlite3
from functools import wraps
from typing import Any, Callable, Iterable, TypeVar, Union

import aiosql
import aiosqlite
from msgspec import Struct
from pypika.queries import QueryBuilder

from ..config import settings

sqlite3.register_adapter(bool, int)
sqlite3.register_converter(
    "BOOLEAN", lambda v: bool(int(v))
)


class Base(
    Struct,
    array_like=True,
    frozen=True,
): ...


queries = aiosql.from_path("queries/", "aiosqlite")

F = TypeVar("F", bound=Callable[..., Any])


def dbmethod(
    func: F,
) -> Callable[..., Any]:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        conn = kwargs.get("conn")

        if conn:
            conn.__class__ = BetterConnection
            return await func(*args, **kwargs)

        async with aiosqlite.connect(
            settings.db_path,
            detect_types=sqlite3.PARSE_DECLTYPES,
        ) as conn:
            conn.__class__ = BetterConnection
            return await func(*args, **kwargs, conn=conn)

    return wrapper  # type: ignore[return-value]


type SQL = str | QueryBuilder


class BetterConnection(aiosqlite.Connection):
    async def execute_raw(
        self, sql: SQL
    ) -> aiosqlite.Cursor:
        if isinstance(sql, QueryBuilder):
            sql = sql.get_sql()

        return await self.execute(sql)

    async def execute_all(
        self, sql: SQL
    ) -> Iterable[aiosqlite.Row]:
        _ = await self.execute_raw(sql)

        return await _.fetchall()

    async def execute_one(
        self, sql: SQL
    ) -> aiosqlite.Row | None:
        _ = await self.execute_raw(sql)
        return await _.fetchone()

    async def execute_scalar(self, sql: SQL) -> Any:
        _ = await self.execute_raw(sql)
        _ = await _.fetchone()

        if _ is None:
            return

        return _[0]
