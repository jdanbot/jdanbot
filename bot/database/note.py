from itertools import chain
from typing import TYPE_CHECKING, Union

from msgspec import convert
from pypika import Query

from ._base import Base, BetterConnection, dbmethod
from ._extras import IsInserted, Unixepoch
from ._tables import N

if TYPE_CHECKING:
    from .member import Member


class Note(Base, frozen=True):
    name: str
    text: str

    @staticmethod
    @dbmethod
    async def get(
        chat_id: int, key: str, conn: BetterConnection
    ) -> Union["Note", None]:
        raw = await conn.execute_one(
            Query.from_(N)
            .select(N.name, N.text)
            .where(N.chat_id == chat_id)
            .where(N.name == key)
        )

        if raw is not None:
            return convert(raw, Note)

    @staticmethod
    @dbmethod
    async def get_notes_list(
        chat_id: int, conn: BetterConnection
    ) -> list[str]:
        notes = await conn.execute_all(
            Query.from_(N)
            .select(N.name)
            .where(N.chat_id == chat_id)
        )

        return convert(
            list(chain.from_iterable(notes)),
            list[str],
        )

    @staticmethod
    @dbmethod
    async def add_or_update(
        editor: Member,
        key: str,
        text: str,
        conn: BetterConnection,
    ) -> bool:
        from pypika import PostgreSQLQuery as Query

        r = await conn.execute_scalar(
            Query.into(N)  # type: ignore[operator]
            .columns(N.chat_id, N.name, N.text, N.author_id)
            .insert(
                editor.chat_id, key, text, editor.user_id
            )
            .on_conflict(N.chat_id, N.name)
            .do_update(N.text, text)
            .do_update(N.editor_id, editor.user_id)
            .do_update(N.updated_at, Unixepoch())
            .returning(IsInserted())
        )

        await conn.commit()
        return bool(r)

    @staticmethod
    @dbmethod
    async def remove(
        chat_id: int, key: str, conn: BetterConnection
    ) -> bool:
        from pypika import PostgreSQLQuery as Query

        r = await conn.execute_scalar(
            Query.from_(N)  # type: ignore[operator]
            .delete()
            .where(N.chat_id == chat_id)
            .where(N.name == key)
            .returning(N.id)
        )

        await conn.commit()
        return (r or 0) > 0
