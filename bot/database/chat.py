from typing import Any, Literal

import aiosqlite
from aiogram import types
from msgspec import Struct, convert, json

from ..config.languages import Language
from ._base import Base, queries


class ChatSettings(Struct, frozen=True):
    enable_welcome: bool = True
    enable_rules: bool = True

    enable_admin: bool = True
    admin_chat: int = 0

    warns_to_ban: Literal[-1, 3, 5] = 3
    enable_selfmute: bool = True
    enable_kick_on_join: bool = False  # polish mode

    enable_poll: bool = True
    enable_triggers: bool = False    # maybe memes?
    enable_twitter_redirect: bool = True

    enable_inline_set_note: bool = False
    enable_extra_poll_option: bool = False

    locked_commands: list[str] = []


class Chat(Base, frozen=True):
    id: int

    title: str
    username: str | None
    language: Language

    current_pidor_id: int | None
    settings: ChatSettings

    welcome: str | None = None
    rules: str | None = None

    @staticmethod
    async def get_by(message: types.Message) -> "Chat":
        if message.from_user is None:
            raise KeyError

        async with aiosqlite.connect("tortoise.db") as conn:
            chat = await queries.chat.get_by(
                conn,
                **message.chat.model_dump(
                    include={
                        "id",
                        "title",
                        "username",
                    }
                ),
            )
            await conn.commit()

        return convert(
            [
                *chat[:3],
                Language.from_str("ru"),
                1,
                json.decode(
                    chat[-1] or "{}",
                    type=ChatSettings,
                    strict=False,
                ),
            ],
            Chat,
        )

    @staticmethod
    async def get(id: int) -> "Chat":
        async with aiosqlite.connect("tortoise.db") as conn:
            chat = await queries.chat.get(conn, id=id)

        return convert(
            [*chat[:3], Language.from_str("ru"), 1, dict()],
            Chat,
        )

    async def set_setting(
        self, setting: str, value: Any
    ) -> bool:
        if value.lower() == "true":
            value = 1
        elif value.lower() == "false":
            value = 0

        async with aiosqlite.connect("tortoise.db") as conn:
            test = await queries.chat.set_setting(
                conn,
                chat_id=self.id,
                key="$." + setting,
                value=value,
            )
            await conn.commit()

            return test
