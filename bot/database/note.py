from typing import TYPE_CHECKING

import aiosqlite
from msgspec import convert

from ._base import Base, queries

if TYPE_CHECKING:
    from .member import Member


class Note(Base, frozen=True):
    name: str
    text: str

    @staticmethod
    async def get(chat_id: int, key: str) -> "Note" | None:
        async with aiosqlite.connect("tortoise.db") as conn:
            raw = await queries.notes.get_note(
                conn, chat_id=chat_id, name=key
            )

            if raw is not None:
                return convert(raw, Note)

    @staticmethod
    async def get_notes_list(chat_id: int) -> list[str]:
        async with aiosqlite.connect("tortoise.db") as conn:
            notes = [
                note
                async for note in queries.notes.get_notes(
                    conn, chat_id=chat_id
                )
            ]

            return convert(
                [note[0] for note in notes],
                list[str],
            )

    @staticmethod
    async def add_or_update(
        editor: Member, key: str, text: str
    ) -> bool:
        async with aiosqlite.connect("tortoise.db") as conn:
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
    async def remove(chat_id: int, key: str) -> bool:
        async with aiosqlite.connect("tortoise.db") as conn:
            r = await queries.notes.delete_note(
                conn=conn,
                chat_id=chat_id,
                name=key,
            )
            await conn.commit()
            return r > 0
