import sqlite3
from datetime import date, datetime
from functools import wraps
from typing import Any, Callable, Iterable, TypeVar

import aiosqlite
from msgspec import Struct
from pypika.queries import QueryBuilder

from ..config import settings

sqlite3.register_adapter(bool, int)
sqlite3.register_converter(
    "BOOLEAN", lambda v: bool(int(v))
)


def date_adapter(object_date: bytes) -> date:
    "receives an object_date in the date adapter for adaptation to the new pattern of sqlite3"
    adapter_format = datetime.fromisoformat(
        object_date.decode("utf-8")
    )
    return adapter_format.date()


sqlite3.register_converter("date", date_adapter)


class Base(
    Struct,
    array_like=True,
    frozen=True,
): ...


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
            sql = sql.get_sql().replace(
                "EXCLUDED", "excluded"
            )

        return await self.execute(sql)

    async def execute_many(self, *sql: SQL):
        for _ in sql:
            await self.execute_raw(_)

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

    async def execute_first(
        self, sql: SQL
    ) -> aiosqlite.Row:
        _ = await self.execute_one(sql)

        if _ is None:
            raise KeyError

        return _

    async def execute_scalar(self, sql: SQL) -> Any:
        _ = await self.execute_raw(sql)
        _ = await _.fetchone()

        if _ is None:
            return

        return _[0]
