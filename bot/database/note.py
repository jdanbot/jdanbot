from typing import TYPE_CHECKING, Union

from msgspec import convert

from ..lib.aiotools import unpack
from ._base import Base, BetterConnection, dbmethod, queries

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
        raw = await queries.notes.get_note(
            conn, chat_id=chat_id, name=key
        )

        if raw is not None:
            return convert(raw, Note)

    @staticmethod
    @dbmethod
    async def get_notes_list(
        chat_id: int, conn: BetterConnection
    ) -> list[str]:
        notes = await unpack(
            queries.notes.get_notes(conn, chat_id=chat_id),
            func=lambda x: x[0],
        )

        return convert(notes, list[str])

    @staticmethod
    @dbmethod
    async def add_or_update(
        editor: Member,
        key: str,
        text: str,
        conn: BetterConnection,
    ) -> bool:
        r = await queries.notes.add_or_update(
            conn=conn,
            chat_id=editor.chat_id,
            name=key,
            text=text,
            author_id=editor.user_id,
        )
        await conn.commit()
        return bool(r)

    @staticmethod
    @dbmethod
    async def remove(
        chat_id: int, key: str, conn: BetterConnection
    ) -> bool:
        r = await queries.notes.delete_note(
            conn=conn,
            chat_id=chat_id,
            name=key,
        )
        await conn.commit()
        return r > 0
